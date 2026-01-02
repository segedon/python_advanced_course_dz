from abc import ABC
from datetime import date


class Room(ABC):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class StandartRoom(Room):
    pass


class LuxuryRoom(Room):
    def __init__(self, name: str, price: float, price_multiplier: float = 1.0):
        super().__init__(name, price)
        self.price *= price_multiplier


class Booking:
    def __init__(self, room: Room, date_: date):
        self.room = room
        self.date = date_


class Hotel:
    def __init__(self, rooms: list[Room] | None = None):
        if rooms is None:
            self.rooms = set()
        else:
            self.rooms = set(rooms)
        self.bookings = []

    def add_room(self, room: Room):
        self.rooms.add(room)

    def get_free_rooms(self, date_: date) -> set[Room]:
        reserved_rooms = set(
            booking.room for booking in self.bookings if booking.date == date_
        )
        return self.rooms - reserved_rooms

    def reserve_room(self, room: Room, date_: date):
        if room not in self.rooms:
            raise ValueError("Данный номер не доступен для бронирования в данном отеле")
        if room not in self.get_free_rooms(date_=date_):
            raise ValueError("Данный номер уже забронирован в указанную дату")
        booking = Booking(room=room, date_=date_)
        self.bookings.append(booking)

    def cancel_booking(self, booking: Booking):
        if booking not in self.bookings:
            raise ValueError("Данное бронирование не относится к отелю")
        self.bookings.remove(booking)

    def get_bookings(self) -> list[Booking]:
        return self.bookings
