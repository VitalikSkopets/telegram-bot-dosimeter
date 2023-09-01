import random
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import create_autospec

import pytest
from telegram import User

from dosimeter.config import config
from dosimeter.constants import Action
from dosimeter.storage import FileRepository

if TYPE_CHECKING:
    from plugins.storage import FileDataFactory, ListTelegramUsers


@pytest.fixture()
def file_repo(tmp_path: Path) -> FileRepository:
    return FileRepository(path_to_file=tmp_path / config.repo.name)


@pytest.mark.file_repo()
class TestFileRepository(object):
    """
    A class for testing logic encapsulated in the FileRepository class.
    """

    mock = create_autospec(FileRepository)

    def test_missing_required_argument(self, tgm_user_factory: User) -> None:
        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mock.put(tgm_user_factory)

        # Assert
        assert exc_info
        assert str(exc_info.value) == "missing a required argument: 'action'"

    def test_missing_attribute(self) -> None:
        # Act
        with pytest.raises(AttributeError) as exc_info:
            self.mock.retrieve()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Mock object has no attribute 'retrieve'"

    @pytest.mark.parametrize("action", list(Action))
    def test_correct_signature(self, tgm_user_factory: User, action: Action) -> None:
        # Act
        result = self.mock.put(tgm_user_factory, action)

        # Assert
        assert result

    def test_create_file_repo(
        self,
        tmp_path: Path,
        data_from_file_repo: "FileDataFactory",
    ) -> None:
        # Arrange
        file = tmp_path / config.repo.name

        # Act
        db = FileRepository(path_to_file=file)
        db_replica = FileRepository(path_to_file=file)

        # Assert
        assert db.__str__() == f"File repository by path: {file}"
        assert db.__str__() == db_replica.__str__()
        assert db_replica.repo.file is db.repo.file
        assert db.repo.file.exists()
        assert db.repo.file.is_file()
        assert db.repo.file.name == config.repo.name
        assert data_from_file_repo(db.repo.file) == {"users": []}

    @pytest.mark.parametrize("action", list(Action))
    def test_put_user(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        action: Action,
        data_from_file_repo: "FileDataFactory",
    ) -> None:
        # Act
        file_repo.put(tgm_user, action)

        # Assert
        data = data_from_file_repo(file_repo.repo.file)
        user_obj = data["users"][0]
        create_at = datetime.strptime(user_obj["create_at"], config.app.date_format)

        assert len(data["users"]) == 1
        assert action in user_obj.keys()
        assert user_obj["user_id"] == tgm_user.id
        assert user_obj["first_name"] != tgm_user.first_name
        assert not user_obj["last_name"]
        assert user_obj["user_name"] != tgm_user.username
        assert isinstance(create_at, datetime)
        assert create_at.date() == date.today()

    def test_put_list_users(
        self,
        file_repo: FileRepository,
        list_tgm_users_factory: "ListTelegramUsers",
        data_from_file_repo: "FileDataFactory",
    ) -> None:
        # Act
        for user in list_tgm_users_factory(5):
            file_repo.put(user, Action.START)

        # Assert
        data = data_from_file_repo(file_repo.repo.file)
        assert len(data["users"]) == 5
        for user_obj in data["users"]:
            assert Action.START in user_obj.keys()

    def test_update_user(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        data_from_file_repo: "FileDataFactory",
    ) -> None:
        # Act
        file_repo.put(tgm_user, Action.HELP)
        file_repo.put(tgm_user, Action.DONATE)
        file_repo.put(tgm_user, Action.HELP)

        # Assert
        data = data_from_file_repo(file_repo.repo.file)
        user_obj = data["users"][0]

        assert len(data["users"]) == 1
        assert Action.START not in user_obj.keys()
        for action in (Action.HELP, Action.DONATE):
            assert action in user_obj.keys()
        assert len(user_obj[Action.HELP]) == 2
        assert len(user_obj[Action.DONATE]) == 1

    @pytest.mark.parametrize("count", [2, 5, 9, 11])
    def test_get_users_count(
        self,
        file_repo: FileRepository,
        count: int,
        list_tgm_users_factory: "ListTelegramUsers",
    ) -> None:
        # Arrange
        list_tgm_users = list_tgm_users_factory(count)

        for user in list_tgm_users:
            file_repo.put(user, random.choice(list(Action)))

        # Act
        result = file_repo.get_count()

        # Assert
        assert result == len(list_tgm_users)
        assert result == count

    def test_get_user(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        list_tgm_users_factory: "ListTelegramUsers",
    ) -> None:
        # Arrange
        list_tgm_users = list_tgm_users_factory(3)
        file_repo.put(tgm_user, Action.DONATE)

        for user in list_tgm_users:
            file_repo.put(user, random.choice(list(Action)))

        # Act
        result = []
        for user in list_tgm_users:
            result.append(file_repo.get(user.id))

        user_from_db = file_repo.get(str(tgm_user.id))

        # Assert
        assert len(result) == 3

        for user_obj in result:
            assert isinstance(user_obj, dict)
            assert isinstance(user_obj["user_id"], int)
            assert isinstance(user_obj["user_name"], str)

        assert user_from_db["user_id"] == tgm_user.id
        assert user_from_db["last_name"] == tgm_user.last_name
        assert Action.DONATE in user_from_db.keys()

    @pytest.mark.parametrize("idf", [00000, 10_000_001])
    def test_get_non_exist_user(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        idf: int,
    ) -> None:
        # Arrange
        file_repo.put(tgm_user, Action.LOCATION)

        # Act
        user_from_file = file_repo.get(idf)

        # Assert
        assert user_from_file == "User does not exist."

    @pytest.mark.parametrize("idf", ["87j24", " 436c", "kH_ejF", ""])
    def test_get_user_by_invalid_id(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        idf: str,
    ) -> None:
        # Arrange
        file_repo.put(tgm_user, Action.ADMIN)

        # Act
        with pytest.raises(ValueError) as exc_info:
            file_repo.get(idf)

        # Assert
        assert exc_info
        assert str(exc_info.value) == "The string must consist of digits."

    @pytest.mark.parametrize("idf", [random.randint(-10_000_000, -1), 2.5, 0.05, None])
    def test_get_user_by_wrong_id(
        self,
        file_repo: FileRepository,
        tgm_user: User,
        idf: int | None,
    ) -> None:
        # Arrange
        file_repo.put(tgm_user, Action.SHOW_CHART)

        # Act
        with pytest.raises(ValueError) as exc_info:
            file_repo.get(idf)

        # Assert
        assert exc_info
        assert str(exc_info.value) == "ID must be an integer, a positive number."

    def test_has_user(
        self,
        file_repo: FileRepository,
        tgm_user: User,
    ) -> None:
        # Arrange
        file_repo.put(tgm_user, random.choice(list(Action)))

        # Act
        has_user = file_repo._has_user(tgm_user.id)

        # Assert
        assert has_user

    @pytest.mark.parametrize("idf", [00000, 10_000_001])
    def test_has_not_user(
        self,
        file_repo: FileRepository,
        list_tgm_users_factory: "ListTelegramUsers",
        idf: int,
    ) -> None:
        # Arrange
        list_tgm_users = list_tgm_users_factory(7)

        for user in list_tgm_users:
            file_repo.put(user, random.choice(list(Action)))

        # Act
        has_user = file_repo._has_user(idf)

        # Assert
        assert not has_user

    def test_create(
        self,
        file_repo: FileRepository,
        tgm_user: User,
    ) -> None:
        # Act
        with mock.patch("dosimeter.storage.file.FileRepository._time_stamp") as mocked:
            mocked.return_value = datetime.now()
            collection = file_repo._create(tgm_user)

        # Assert
        assert not collection

    def test_delete_file_repo(
        self,
        file_repo: FileRepository,
    ) -> None:
        # Act
        file_repo.repo.delete()

        # Assert
        assert not file_repo.repo.file.exists()

    def test_delete_file_repo_with_raise_exc(
        self,
        file_repo: FileRepository,
    ) -> None:
        # Arrange
        file_repo.repo.delete()

        # Act
        with pytest.raises(ValueError) as exc_info:
            file_repo.repo.delete()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "File not exist."
