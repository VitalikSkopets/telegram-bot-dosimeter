import json
from pathlib import Path
from typing import Any, Mapping, TypeAlias

from dosimeter.config.logging import get_logger

logger = get_logger(__name__)

FileDataType: TypeAlias = Mapping[str, Any]


class ValidationError(ValueError):
    pass


class JSONFileManager(object):
    """
    Class, which is an interface for creating, reading, writing and deleting JSON files.
    """

    READ_ONLY = "r"
    WRITE_ONLY = "w"

    def __init__(self, path_to_file: Path = Path("data.json")) -> None:
        """
        Constructor method for initializing objects of class JSONFileManager.
        """
        self.file = path_to_file

        if Path(self.file).exists():
            return

        self.file.touch()
        self.write(data={})
        logger.debug("Init new JSON file object.")

    def read(self) -> FileDataType:
        """
        Public method for reading a json file.
        """
        if self.file.exists() and self._is_valid():
            logger.debug("Process reading file...")
            try:
                with open(self.file, self.READ_ONLY) as file:
                    return json.load(file)
            except json.JSONDecodeError as exc:
                logger.exception(
                    "Deserializable data won't be a valid JSON "
                    "document. Raised exception: %s" % exc
                )
                exit(1)

        raise ValidationError("File not exist.")

    def write(self, data: FileDataType) -> None:
        """
        Public method for writing to a json file.
        """
        if self.file.exists() and self._is_valid() or not self.file.exists():
            logger.debug("Process writing file...")
            try:
                with open(self.file, self.WRITE_ONLY) as file:
                    json.dump(data, file, indent=2)
            except json.JSONDecodeError as exc:
                logger.exception(
                    "Objects cannot be serialized. Raised exception: %s" % exc
                )
                exit(1)

            logger.debug("The data has been successfully written to the file.")

    def delete(self) -> None:
        """
        Public method for deleting a json file.
        """
        if self.file.exists() and self._is_valid():
            self.file.unlink()
            logger.debug("File was successfully deleted.")
            return None

        raise ValidationError("File not exist.")

    def _is_valid(self) -> bool:
        """
        Private json file validation method.
        """
        logger.debug("Process validating file...")
        if self.file.is_file() and self.file.suffix in (".json", ".JSON"):
            logger.debug("Validation was successful.")
            return True

        raise ValidationError(
            "File must have '.json' extension or is it not a file object."
        )
