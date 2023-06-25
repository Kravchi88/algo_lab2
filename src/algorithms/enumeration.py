from src.models.rectangle import Point, Rectangle


class EnumerationAlgorithm:
    def __init__(self, rectangles: list[Rectangle]):
        self.rectangles = rectangles

    def get_count_rectangles(self, point: Point) -> int:
        count = 0
        for rectangle in self.rectangles:
            if rectangle.point_in_rectangle(point):
                count += 1
        return count
