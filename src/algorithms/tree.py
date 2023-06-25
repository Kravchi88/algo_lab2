from src.models.rectangle import Rectangle
from src.models.point import Point
from src.models.operation import Operation
from src.models.persistent_tree import PersistentTree
from src.algorithms.compression import CoordinateCompressor

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