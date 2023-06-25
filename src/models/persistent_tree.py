from dataclasses import dataclass, field
from src.models.operation import Operation
from typing import Optional

@dataclass
class Node:
    start: int
    end: int
    modifier: int = field(default=0)
    left: Optional["Node"] = field(default=None)
    right: Optional["Node"] = field(default=None)

    def copy(self) -> "Node":
        return Node(self.start, self.end, self.modifier, self.left, self.right)


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

