from typing import List, Optional


class ListNode:
    def __init__(self, val: int, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return False
        return self.val == other.val and self.next == other.next

    def __repr__(self):
        return f"ListNode(val={self.val}, next={repr(self.next)})"


# Helper function for testing
def to_list(values: List[int]) -> Optional[ListNode]:
    current: Optional[ListNode] = None
    for value in reversed(values):
        current = ListNode(value, next=current)
    return current


# Macro equivalent
def linked(*args: int) -> Optional[ListNode]:
    return to_list(list(args))
