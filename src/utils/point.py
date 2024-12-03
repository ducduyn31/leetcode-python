class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


# Helper function to create a Point (replacing the Rust macro)
def point(*args: int) -> "Point":
    if len(args) != 2:
        raise ValueError("Point requires exactly two arguments: x and y.")
    return Point(args[0], args[1])
