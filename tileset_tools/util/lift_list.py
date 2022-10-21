from typing import TypeVar


T = TypeVar("T")


def lift_list(val: T | list[T]) -> list[T]:
    match val:
        case list():
            return val  # type: ignore
        case _:
            return [val]

def try_flatten(val: list[T]) -> T | list[T]:
    match val:
        case [x]:
            return x
        case _:
            return val
