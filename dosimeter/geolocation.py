from geopy import distance

from dosimeter.constants import Points

__all__ = ("get_nearest_point_location",)


def get_nearest_point_location(
    latitude: float | None = None, longitude: float | None = None
) -> tuple[float, str]:
    """
    The function calculates the minimum distance in meters relative to the user's
    location to the nearest monitoring point
    """
    user_coordinates = (latitude, longitude)
    distance_list = [
        (
            round(distance.distance(user_coordinates, point.coordinates).m, 3),
            point.label,
        )
        for point in Points
    ]
    return min(distance_list)
