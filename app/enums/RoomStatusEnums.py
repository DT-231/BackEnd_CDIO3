from enum import Enum


class RoomStatusEnums(str, Enum):

    AVAILABLE = "available"  # this room is available for booking
    BOOKED = "Booked"  # this room is currently booked
    DIRTY = "Dirty "  # this room needs cleaning
    CLEAR = "Clean"  # this room is clean and ready for booking
