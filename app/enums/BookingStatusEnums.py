from enum import Enum


class BookingStatusEnums(str, Enum):

    PENDING = "pending"  # this status of booking  is pending when the user has not yet confirmed the booking
    CONFIRMED = "confirmed"  # this status of booking is confirmed when the user has payment the booking
    CANCELLED = "cancelled"  # this status of booking is cancelled when the user has cancelled the booking
    COMPLETED = "completed"  # this status of booking is completed when the user has check out the booking
