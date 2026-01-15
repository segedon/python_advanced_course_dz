import sys


class User:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
    ):
        self.name = name
        self.email = email
        self.password = password


class SlotUser:
    __slots__ = (
        "name",
        "email",
        "password",
    )

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


def get_full_size(obj, seen=None):
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if hasattr(obj, "__dict__"):
        for attr, value in obj.__dict__.items():
            if not isinstance(value, (int, float, bool, str, bytes)):
                size += get_full_size(value, seen)
            else:
                size += sys.getsizeof(value)
            size += sys.getsizeof(attr)

    if hasattr(obj, "__slots__"):
        for slot in obj.__slots__:
            if hasattr(obj, slot):
                value = getattr(obj, slot)
                size += get_full_size(value, seen)

    return size


if __name__ == "__main__":
    users = [
        User(name="test", email="test@test.test", password="test")
        for _ in range(100_000)
    ]
    slot_users = [
        SlotUser(name="test", email="test@test.test", password="test")
        for _ in range(100_000)
    ]
    print(
        "Размер объектов без __slots__ в байтах: ",
        sum(get_full_size(user) for user in users),
    )
    print(
        "Размер объектов с __slots__ в байтах",
        sum(get_full_size(user) for user in slot_users),
    )
