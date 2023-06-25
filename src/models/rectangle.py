from dataclasses import dataclass
from src.models.point import Point


@dataclass
class Rectangle:
    start: Point
    end: Point

    def point_in_rectangle(self, point: Point) -> bool:
        return (self.start.x <= point.x < self.end.x) and (
            self.start.y <= point.y < self.end.y
        )
