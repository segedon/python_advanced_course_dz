from typing import TypeVar, Generic
from collections.abc import Hashable


Key = TypeVar("Key", bound=Hashable)
Value = TypeVar("Value")


class Cache(Generic[Key, Value]):
    def __init__(self):
        self.__cache: dict[Key, Value] = {}

    def set(self, key: Key, value: Value) -> None:
        self.__cache[key] = value

    def get(self, key: Key) -> Value | None:
        return self.__cache.get(key, None)

    def keys(self) -> list[Key]:
        return list(self.__cache.keys())

    def values(self) -> list[Value]:
        return list(self.__cache.values())


if __name__ == "__main__":
    hits = Cache[str, int]()
    hits.set("home", 3)
    hits.set("about", 3)
    print(hits.get("home"))
    print(hits.keys())
    print(hits.values())
