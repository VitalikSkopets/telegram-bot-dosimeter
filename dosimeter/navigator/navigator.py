from typing import TypeAlias

from geopy import distance

from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import Points
from dosimeter.storage import manager_admins as manager

__all__ = ("Navigator",)

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})

Latitude: TypeAlias = float
Longitude: TypeAlias = float
Distance: TypeAlias = float


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

    def get_min_distance(
        self,
        user_id: int,
        latitude: Latitude = 0.0,
        longitude: Longitude = 0.0,
    ) -> tuple[Distance, str]:
        """
        The method calculates the minimum distance in meters relative to the user's
        location to the nearest monitoring point.
        """
        user_coordinates = (latitude, longitude)
        logger.debug(
            "User coordinates - Latitude: %f Longitude: %f" % (latitude, longitude),
            user_id=manager.get_one(user_id),
        )

        try:
            distance_list = [
                (
                    round(self.distance(user_coordinates, point.coordinates).m, 3),
                    point.label,
                )
                for point in Points
            ]
        except Exception as ex:
            logger.exception(
                "Unable to calculates the min distance. Raised exception: %s" % ex,
                user_id=manager.get_one(user_id),
            )
            raise

        return min(distance_list)
