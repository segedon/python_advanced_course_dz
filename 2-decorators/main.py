from typing import Literal

from functools import wraps


def limit_args(max_value: int, mode: Literal["error", "clip"]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            numeric_types = (int, float)
            if mode == "clip":
                args = (
                    min(arg, max_value) if isinstance(arg, numeric_types) else arg
                    for arg in args
                )
                kwargs = {
                    key: min(value, max_value)
                    if isinstance(value, numeric_types)
                    else value
                    for key, value in kwargs.items()
                }

            elif mode == "error":
                if not all(
                    arg <= max_value for arg in args if isinstance(arg, numeric_types)
                ):
                    raise ValueError(
                        f"All argument must be letter or equal {max_value}"
                    )
                if not all(
                    value <= max_value
                    for key, value in kwargs.items()
                    if isinstance(value, numeric_types)
                ):
                    raise ValueError(
                        f"All argument must be letter or equal {max_value}"
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator
