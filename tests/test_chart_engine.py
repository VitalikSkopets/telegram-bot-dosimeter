import pathlib
import random
from unittest.mock import create_autospec

import pytest
from _pytest.fixtures import SubRequest
from plugins.parsing import assign_id

from dosimeter.chart_engine import ChartEngine
from dosimeter.constants import Point, Region
from dosimeter.parser import RegionInfoDTO


@pytest.fixture(params=list(Region), ids=assign_id)
def region_info_dto(request: SubRequest) -> RegionInfoDTO:
    """
    Generating RegionInfoDTO object.
    """
    region_data = {
        point.label: round(random.random(), 2)
        for point in Point
        if point.region == request.param
    }

    return RegionInfoDTO(region=request.param, info=region_data)


@pytest.mark.chart_engine()
class TestChartEngine(object):
    """
    A class for testing logic encapsulated in the ChartEngine class.
    """

    mock = create_autospec(ChartEngine)
    dir = "charts"

    def test_missing_required_argument(self) -> None:
        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mock.create()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "missing a required argument: 'data'"

    def test_missing_attribute(self) -> None:
        # Act
        with pytest.raises(AttributeError) as exc_info:
            self.mock.update()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Mock object has no attribute 'update'"

    def test_correct_signature(self, region_info_dto: RegionInfoDTO) -> None:
        # Act
        result = self.mock.create(region_info_dto)

        # Assert
        assert result

    def test_create_success(
        self,
        tmp_path: pathlib.Path,
        region_info_dto: RegionInfoDTO,
    ) -> None:
        # Arrange
        bar_chart = ChartEngine(dir_path=tmp_path / self.dir)

        # Act
        bar_chart.create(region_info_dto)
        file = tmp_path / self.dir / ChartEngine.file_name

        # Assert
        assert file.exists()
        assert file.is_file()
        assert file.suffix == ".png"
        assert file.name == ChartEngine.file_name
        assert str(file.parent).endswith(self.dir)

    def test_delete_success(
        self,
        tmp_path: pathlib.Path,
        region_info_dto: RegionInfoDTO,
    ) -> None:
        # Arrange
        bar_chart = ChartEngine(dir_path=tmp_path / self.dir)

        # Act
        bar_chart.create(region_info_dto)
        file = tmp_path / self.dir / ChartEngine.file_name
        bar_chart.delete()

        # Assert
        assert not file.exists()
