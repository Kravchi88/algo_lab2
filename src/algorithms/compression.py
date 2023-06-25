from src.models.point import Point
from src.models.rectangle import Rectangle


class CoordinateCompressor:
    x: list[int]
    y: list[int]

    def __init__(self, points: list[Point]):
        self.x = []
        self.y = []

        for point in points:
            self.x.append(point.x)
            self.y.append(point.y)
        self.x.sort()
        self.y.sort()

    def get_compressed_point(self, point: Point) -> Point:
        x = left_binary_search(self.x, point.x)
        y = left_binary_search(self.y, point.y)
        return Point(x, y)

    def get_compressed_rectangle(self, rectangle: Rectangle) -> Rectangle:
        return Rectangle(
            self.get_compressed_point(rectangle.start),
            self.get_compressed_point(rectangle.end),
        )
        
    def get_compressed_rectangles(self, rectangles: list[Rectangle]) -> list[Rectangle]:
        return [self.get_compressed_rectangle(rectangle) for rectangle in rectangles]


def left_binary_search(arr, x):
    start = 0
    end = len(arr) - 1
    mid = 0

    while start <= end:
        mid = (end + start) // 2

        if arr[mid] > x:
            end = mid - 1
        else:
            start = mid + 1

    return end


def main():
    rectangles = [
        Rectangle(Point(15, 20), Point(318, 43)),
        Rectangle(Point(9, 28), Point(59, 61)),
    ]
    rectangles_points = []
    for rectangle in rectangles:
        rectangles_points.append(rectangle.start)
        rectangles_points.append(rectangle.end)
    compressor = CoordinateCompressor(rectangles_points)

    for rectangle in rectangles:
        print(compressor.get_compressed_rectangle(rectangle))


if __name__ == "__main__":
    main()
