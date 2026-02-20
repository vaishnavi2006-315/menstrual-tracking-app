from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CycleRecord:
    start_date: date
    cycle_length: int
