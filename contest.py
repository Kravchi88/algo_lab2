from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Rectangle:
    start: Point
    end: Point

    def point_in_rectangle(self, point: Point) -> bool:
        return (self.start.x <= point.x < self.end.x) and (
            self.start.y <= point.y < self.end.y
        )

@dataclass
class Operation:
    start: int
    end: int
    operator: int


@dataclass
class Node:
    start: int
    end: int
    modifier: int = field(default=0)
    left: Optional["Node"] = field(default=None)
    right: Optional["Node"] = field(default=None)

    def copy(self) -> "Node":
        return Node(self.start, self.end, self.modifier, self.left, self.right)
    

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



class Tree:
    def __init__(self, start: int, end: int):
        """
        Создаём дерево
        """

        def createTree(l, r):
            if l > r:
                return None

            if l == r:
                n = Node(l, r)
                return n

            mid = (l + r) // 2

            root = Node(l, r)

            root.left = createTree(l, mid)
            root.right = createTree(mid + 1, r)

            return root

        self.root = createTree(start, end)

    def do_operation(self, operation: Operation) -> None:
        """
        Метод производящий операцию на интервале [start, end]
        """

        def do_operation_impl(root: Optional[Node], operation: Operation):
            if root is None:
                return

            if operation.start > root.end:
                return

            if operation.end < root.start:
                return

            if operation.start <= root.start and operation.end >= root.end:
                root.modifier += operation.operator
                return

            do_operation_impl(root.left, operation)
            do_operation_impl(root.right, operation)

        do_operation_impl(self.root, operation)

    def get_leaf_modifier(self, leaf: int) -> int:
        """
        Метод для получения модификатора для листа дерева
        """

        def get_leaf_modifier_impl(root: Optional[Node], leaf: int) -> int:
            if root is None:
                return 0

            if leaf < root.start or leaf > root.end:
                return 0

            return (
                root.modifier
                + get_leaf_modifier_impl(root.left, leaf)
                + get_leaf_modifier_impl(root.right, leaf)
            )

        return get_leaf_modifier_impl(self.root, leaf)


class PersistentTree:
    trees: list[Tree]

    def __init__(self, operations: list[Operation]):
        self.trees = []

        leafs_count = len(operations) - 1
        tree = Tree(0, leafs_count)
        tree.do_operation(operations[0])
        self.trees.append(tree)

        for operation in operations[1:]:
            new_tree = self.__create_next_tree(self.trees[-1], operation)
            self.trees.append(new_tree)

    def __create_next_tree(self, prev_tree: Tree, operation: Operation) -> Tree:
        tree = Tree(0, 0)

        def build(root: Optional[Node], operation: Operation) -> Optional[Node]:
            if root is None:
                return None

            if operation.start > root.end or operation.end < root.start:  # Нет покрытия
                return root

            if (
                operation.start <= root.start and root.end <= operation.end
            ):  # Полное покрытие
                node = root.copy()
                node.modifier += operation.operator
                return node

            
            # Частичное покрытие
            node = root.copy()
            node.left = build(node.left, operation)
            node.right = build(node.right, operation)

            return node

        tree.root = build(prev_tree.root, operation)
        return tree


class TreeAlgorithm:
    def __init__(self, rectangles: list[Rectangle]):
        self.compressor = self.__init_compressor(rectangles)
        self.tree = self.__init_tree(rectangles)
        

    def __init_compressor(self, rectangles: list[Rectangle]) -> CoordinateCompressor:
        rectangles_points = []
        for rectangle in rectangles:
            rectangles_points.append(rectangle.start)
            rectangles_points.append(rectangle.end)

        return CoordinateCompressor(rectangles_points)
    
    def __init_tree(self, rectangles: list[Rectangle]) -> PersistentTree:
        compressed_rectangles = self.compressor.get_compressed_rectangles(rectangles)
        compressed_rectangles.sort(key=lambda x: x.start.x)
        
        unsorted_operations = []
        for rectangle in compressed_rectangles:
            unsorted_operations.append((rectangle.start.x, Operation(rectangle.start.y, rectangle.end.y-1, 1)))
            unsorted_operations.append((rectangle.end.x, Operation(rectangle.start.y, rectangle.end.y-1, -1)))
        
        unsorted_operations.sort(key=lambda x: x[0])
        
        operations = []
        for _, operation in unsorted_operations:
            operations.append(operation)
        
        return PersistentTree(operations)

    def get_count_rectangles(self, point: Point) -> int:
        compressed_point = self.compressor.get_compressed_point(point)
        return self.tree.trees[compressed_point.x].get_leaf_modifier(compressed_point.y)

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
    
    
    if len(rectangles) == 0 or len(points) == 0:
        return

    tree_result = use_algorithm(TreeAlgorithm, rectangles, points)
    print(*tree_result)
    
if __name__ == "__main__":
    main()
