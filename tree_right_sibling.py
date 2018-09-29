import functools

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class BinaryTreeNode:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.next = None  # Populates this field.


def construct_right_sibling(tree):
    '''
    if not tree:
        return
    nodes = [tree]
    while nodes:
        temp = []
        for node in nodes:
            if node.left:
                node.left.next = node.right
                if node.next:
                    node.right.next = node.next.left
                temp += [node.left, node.right]
        nodes = temp
    return
    '''

    while tree and tree.left:
        left_most = tree
        while tree and tree.left:
            tree.left.next = tree.right
            if tree.next:
                tree.right.next = tree.next.left
            tree = tree.next   # go to the next node in the same level
        tree = left_most.left  # go to the next left node in the next level

def traverse_next(node):
    while node:
        yield node
        node = node.next
    raise StopIteration


def traverse_left(node):
    while node:
        yield node
        node = node.left
    raise StopIteration


def clone_tree(original):
    if not original:
        return None
    cloned = BinaryTreeNode(original.data)
    cloned.left, cloned.right = clone_tree(original.left), clone_tree(
        original.right)
    return cloned


@enable_executor_hook
def construct_right_sibling_wrapper(executor, tree):
    cloned = clone_tree(tree)

    executor.run(functools.partial(construct_right_sibling, cloned))

    return [[n.data for n in traverse_next(level)]
            for level in traverse_left(cloned)]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("tree_right_sibling.py",
                                       'tree_right_sibling.tsv',
                                       construct_right_sibling_wrapper))