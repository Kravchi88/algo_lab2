from src.models.point import Point
from src.models.rectangle import Rectangle

from src.algorithms.enumeration import EnumerationAlgorithm
from src.algorithms.map import MapAlgorithm
from src.algorithms.tree import TreeAlgorithm



def use_algorithm(
    algorithm, rectangles: list[Rectangle], points: list[Point]
) -> list[int]:
    algorithm = algorithm(rectangles)
    result = []
    for point in points:
        result.append(algorithm.get_count_rectangles(point))

    return result


def main():
    n = int(input())
    rectangles = []
    for _ in range(n):
        cords = list(map(int, input().split()))
        start = Point(cords[0], cords[1])
        end = Point(cords[2], cords[3])
        rectangles.append(Rectangle(start, end))

    m = int(input())
    points = []
    for _ in range(m):
        cords = list(map(int, input().split()))
        points.append(Point(cords[0], cords[1]))

    enum_result = use_algorithm(EnumerationAlgorithm, rectangles, points)
    print(enum_result)

    map_result = use_algorithm(MapAlgorithm, rectangles, points)
    print(map_result)

    tree_result = use_algorithm(TreeAlgorithm, rectangles, points)
    print(tree_result)
    
if __name__ == "__main__":
    main()
