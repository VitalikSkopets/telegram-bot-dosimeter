from typing import NamedTuple, TypeAlias

from geopy import distance

from dosimeter.admin import manager
from dosimeter.config.logging import CustomAdapter, get_logger
from dosimeter.constants import Point

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})

Latitude: TypeAlias = float
Longitude: TypeAlias = float
Distance: TypeAlias = float


class NearPoint(NamedTuple):
    distance: float
    title: str


class Navigator(object):
    """
    A class in which the logic of calculating the minimum distance by user coordinates
    is implemented.
    """

    def __init__(self) -> None:
        """
        Constructor method for initializing objects of class Navigator.
        """
        self.distance = distance.distance

    def get_near_point(
        self,
        user_id: int,
        latitude: Latitude = 0.0,
        longitude: Longitude = 0.0,
    ) -> NearPoint:
        """
        The method calculates the minimum distance in meters relative to the user's
        location to the nearest monitoring point.
        """
        user_coordinates = (latitude, longitude)

        logger.debug(
            "User coordinates - Latitude: %f Longitude: %f" % (latitude, longitude),
            user_id=manager.get_one(user_id),
        )

        distance_list = [
            (
                round(self.distance(user_coordinates, point.coordinates).m, 3),
                point.label,
            )
            for point in Point
        ]

        return NearPoint(*min(distance_list))
