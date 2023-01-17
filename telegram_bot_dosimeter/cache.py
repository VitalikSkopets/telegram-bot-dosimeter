from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Any, Callable

__all__ = ("timed_lru_cache",)


def timed_lru_cache(seconds: int, maxsize: int = 128) -> Callable:
    """The cache returns the result to the request only if the record caching
    period has not expired yet.
    """

    def wrapper_cache(func: Callable) -> Callable:
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)  # type: ignore[attr-defined]
        func.expiration = datetime.utcnow() + func.lifetime  # type: ignore

        @wraps(func)
        def wrapped_func(*args: Any, **kwargs: Any) -> Callable:
            if datetime.utcnow() >= func.expiration:  # type: ignore[attr-defined]
                func.cache_clear()  # type: ignore[attr-defined]
                func.expiration = datetime.utcnow() + func.lifetime  # type: ignore

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
