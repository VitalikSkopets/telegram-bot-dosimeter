from geopy import distance

from telegram_bot_dosimeter.constants import MONITORING_POINTS

__all__ = ("get_nearest_point_location",)


def get_nearest_point_location(
    latitude: float | None = None, longitude: float | None = None
) -> tuple[float, str]:
    """
    The function calculates the minimum distance in meters relative to the user's
    location to the nearest monitoring point
    :param latitude: user latitude coordinate
    :param longitude: user latitude longitude
    :return: tuple containing the distance in meters to the nearest monitoring point
    and the name of the monitoring point
    """
    user_coordinates = (latitude, longitude)
    distance_list = []
    for point in MONITORING_POINTS:
        distance_list.append(
            (
                round(distance.distance(user_coordinates, point.coordinates).m, 3),
                point.name,
            ),
        )
    return min(distance_list)
