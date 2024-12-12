class Node:
    """A node of a singly-linked list."""
    def __init__(self, value=None, tail=None):
        self.value = value
        self.tail = tail

    def __str__(self):
        return str(self.value)


class List:
    """A basic singly-linked (forward) list.

    This type of List is suitable for FIFO queues and ... not a lot else
    really. It supports appending to the end of the list, inserting (to the
    front of the list only), and popping elements off the front of the list.
    Other operations like inserting at an aribtrary index, or popping from the
    end of the list, are not supported.
    """
    def __init__(self, values: tuple | list | None = None):
        self.start = None
        self.end = None
        self.length = 0
        if values:
            self.extend(values)

    def __len__(self):
        return self.length

    def __str__(self):
        return ','.join(x for x in self)

    def __iter__(self):
        node = self.start
        while node is not None:
            yield node.value
            node = node.tail

    def append(self, value) -> Node:
        node = Node(value)
        if self.end is not None:
            self.end.tail = node
        if self.start is None:
            self.start = node
        self.end = node
        self.length += 1
        return node

    def extend(self, values):
        """Extend this list by appending each element from `values`."""
        prev = self.end
        for value in values:
            node = Node(value)
            if self.start is None:
                self.start = node
            if prev is not None:
                prev.tail = node
            prev = node
            self.length += 1
        self.end = prev

    def insert(self, value):
        """Insert a value at the front of the list."""
        node = Node(value, self.start)
        self.start = node
        self.length += 1

    def popleft(self):
        """Remove and return a value from the front of the list."""
        node = self.start
        if node is None:
            raise IndexError("popleft from empty List")
        self.start = node.tail
        self.length -= 1
        return node.value


class DoubleNode(Node):
    """A node of a doubly-linked list."""
    def __init__(self, value=None, head=None, tail=None):
        self.value = value
        self.head = head
        self.tail = tail


class DoubleList(List):
    """A doubly-linked list.

    This type of list is suitable when you want to arbitrarily add and remove
    elements from any part of a list without having to reindex the whole thing.
    For small lists, the native Python `list` will work fine, but for lists
    with a lot of elements the doubly linked list might be a win.

    It supports all the operations of the singly-linked List, plus it can also
    iterate backwards, and pop elements off the end of the list.
    """
    def append(self, value) -> DoubleNode:
        """Add an item to the end of the list.

        Return the newly created DoubleNode object.
        """
        node = DoubleNode(value, self.end)
        if self.end is not None:
            self.end.tail = node
        if self.start is None:
            self.start = node
        self.end = node
        self.length += 1
        return node

    def extend(self, values):
        """Add items to the end of this list from `values`."""
        prev = self.end
        for value in values:
            node = DoubleNode(value, prev)
            if self.start is None:
                self.start = node
            if prev is not None:
                prev.tail = node
            prev = node
            self.length += 1
        self.end = prev

    def insert(self, value, node: DoubleNode | None = None) -> DoubleNode:
        """Insert a new node into this list.

        If `node` is provided, insert the new node immediately before that
        node. Otherwise, insert it at the front of the list.

        Return the newly created DoubleNode object.

        Caution: it is the caller's responsibility to make sure that any `node`
        passed into this function is actually a member of this list. Passing a
        node that is not a member of the list will lead to invalid results.
        """
        if node is None:
            # Insert at the start
            result = DoubleNode(value, None, self.start)
            if self.start is not None:
                self.start.head = result
            self.start = result
            if self.end is None:
                self.end = result
            self.length += 1
            return result

        result = DoubleNode(value, node.head, node)
        if node.head is None:
            self.start = result
        else:
            node.head.tail = result
        node.head = result
        self.length += 1
        return result

    def pop(self):
        """Remove and return the value from the end of the list.

        Raises IndexError if the list is empty.
        """
        if self.end is None:
            raise IndexError("Cannot pop() from an empty DoubleList")
        node = self.end
        self.end = node.head
        if node.head is None:
            self.start = None
        else:
            node.head.tail = node.tail
        if node.tail is not None:
            node.tail.head = node.head
        self.length -= 1
        return node.value

    def popleft(self):
        """Remove and return the value from the front of the list.

        Raises IndexError if the list is empty.
        """
        if self.start is None:
            raise IndexError("Cannot popleft() from an empty DoubleList")

        node = self.start
        self.start = node.tail

        if node.tail is None:
            self.end = None
        else:
            node.tail.head = None

        self.length -= 1
        return node.value

    def remove(self, node: DoubleNode):
        """Remove `node` from this list, and return its value.

        Caution: it is the caller's responsibility to make sure that any `node`
        passed into this function is actually a member of this list. Passing a
        node that is not a member of the list will lead to invalid results.
        """
        if node.head is None:
            self.start = node.tail
        else:
            node.head.tail = node.tail

        if node.tail is None:
            self.end = node.head
        else:
            node.tail.head = node.head

        self.length -= 1
        return node.value
