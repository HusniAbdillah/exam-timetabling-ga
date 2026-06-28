from dataclasses import dataclass


@dataclass(frozen=True)
class Timeslot:
    """Represents a scheduled exam timeslot.

    Attributes:
        slot_id: Unique integer identifier for the slot (1-indexed).
        day: The day of the exam (e.g., 1 to 5).
        session: The session of the day (e.g., 1 to 3).
    """

    slot_id: int
    day: int
    session: int
