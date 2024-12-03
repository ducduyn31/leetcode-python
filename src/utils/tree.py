from collections import deque
from typing import List, Optional, Union


class TreeNode:
    def __init__(
        self,
        val: int,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return (
            self.val == other.val
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        return f"TreeNode(val={self.val}, left={repr(self.left)}, right={repr(self.right)})"


def to_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Converts a list of values to a binary tree using level-order traversal."""
    if not values or values[0] is None:
        return None

    iter_values = iter(values)
    root = TreeNode(next(iter_values))
    queue = deque([root])

    for val in iter_values:
        current = queue.popleft()
        if val is not None:
            current.left = TreeNode(val)
            queue.append(current.left)
        try:
            val = next(iter_values)
            if val is not None:
                current.right = TreeNode(val)
                queue.append(current.right)
        except StopIteration:
            break

    return root


# Macro equivalent for constructing a tree
def tree(*args: Union[int, None]) -> Optional[TreeNode]:
    """Creates a tree from the given arguments."""
    return to_tree(list(args))
