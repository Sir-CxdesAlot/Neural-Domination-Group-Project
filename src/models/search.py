"""
models/search.py
================
Generic search primitives shared by Part 1 (flight connections).

Classes
-------
Node            A state + its parent + the action that created it.
StackFrontier   LIFO frontier → Depth-First Search.
QueueFrontier   FIFO frontier → Breadth-First Search (shortest path).
"""


class Node:
    """
    A single node in the search tree.

    Attributes
    ----------
    state  : any hashable  – the city_id at this node
    parent : Node | None   – the node we came from (None for the root)
    action : tuple | None  – (flight_id, city_id) that produced this node
    """

    __slots__ = ("state", "parent", "action")

    def __init__(self, state, parent, action):
        self.state  = state
        self.parent = parent
        self.action = action

    def __repr__(self):
        return f"Node(state={self.state!r}, action={self.action!r})"


class StackFrontier:
    """
    LIFO frontier – implements Depth-First Search.

    Methods
    -------
    add(node)              Push node onto the stack.
    remove()               Pop the most-recently-added node.
    contains_state(state)  O(n) membership test.
    empty()                True when the frontier has no nodes.
    """

    def __init__(self):
        self._frontier: list[Node] = []

    # ------------------------------------------------------------------ #
    def add(self, node: Node) -> None:
        self._frontier.append(node)

    def remove(self) -> Node:
        if self.empty():
            raise IndexError("Cannot remove from an empty frontier.")
        return self._frontier.pop()

    def contains_state(self, state) -> bool:
        return any(n.state == state for n in self._frontier)

    def empty(self) -> bool:
        return len(self._frontier) == 0

    def __len__(self) -> int:
        return len(self._frontier)

    def __repr__(self) -> str:
        return f"StackFrontier(size={len(self)})"


class QueueFrontier(StackFrontier):
    """
    FIFO frontier – implements Breadth-First Search.

    Overrides only `remove` to pop from the *front* of the list,
    guaranteeing the shortest path (fewest hops) is found first.
    """

    def remove(self) -> Node:
        if self.empty():
            raise IndexError("Cannot remove from an empty frontier.")
        return self._frontier.pop(0)   # front → BFS

    def __repr__(self) -> str:
        return f"QueueFrontier(size={len(self)})"