from src.models.rectangle import Rectangle
from src.models.point import Point
from src.algorithms.compression import CoordinateCompressor


class MapAlgorithm:
    def __init__(self, rectangles: list[Rectangle]):
        self.compressor = self.__init_compressor(rectangles)
        self.map: list[list[int]] = self.__init_map(rectangles)

    def __init_compressor(self, rectangles: list[Rectangle]) -> CoordinateCompressor:
        rectangles_points = []
        for rectangle in rectangles:
            rectangles_points.append(rectangle.start)
            rectangles_points.append(rectangle.end)

        return CoordinateCompressor(rectangles_points)

    def __init_map(self, rectangles: list[Rectangle]) -> list[list[int]]:
        rectangles_map = [
            [0 for _ in range(0, len(self.compressor.y))]
            for _ in range(0, len(self.compressor.x))
        ]

        for rectangle in rectangles:
            compressed_rectangle = self.compressor.get_compressed_rectangle(rectangle)
            for x in range(compressed_rectangle.start.x, compressed_rectangle.end.x):
                for y in range(
                    compressed_rectangle.start.y, compressed_rectangle.end.y
                ):
                    rectangles_map[x][y] += 1

        return rectangles_map

    def get_count_rectangles(self, point: Point) -> int:
        compressed_point = self.compressor.get_compressed_point(point)
        return self.map[compressed_point.x][compressed_point.y]
