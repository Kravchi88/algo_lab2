from dataclasses import dataclass


@dataclass
class Operation:
    start: int
    end: int
    operator: int
