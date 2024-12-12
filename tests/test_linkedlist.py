import pytest

import linkedlist


def test_list_init():
    # By default, the initialiser should create an empty List
    a = linkedlist.List()
    assert a.length == 0

    a = linkedlist.List(['a', 'b', 'c'])
    assert a.length == 3


def test_list_len():
    a = linkedlist.List()
    assert len(a) == 0

    a = linkedlist.List(['a', 'b', 'c'])
    assert len(a) == 3


def test_list_iter():
    a = linkedlist.List()
    assert tuple(x for x in a) == tuple()

    a = linkedlist.List(['a', 'b', 'c'])
    assert tuple(x for x in a) == ('a', 'b', 'c')


def test_list_append():
    # Append to empty list
    a = linkedlist.List()
    a.append('a')
    assert len(a) == 1
    assert tuple(x for x in a) == ('a',)

    # Append to non-empty list
    a = linkedlist.List(['a', 'b', 'c'])
    a.append('d')
    assert len(a) == 4
    assert tuple(x for x in a) == ('a', 'b', 'c', 'd')


def test_list_extend():
    # Extend empty list
    a = linkedlist.List()
    a.extend(('a', 'b'))
    assert len(a) == 2
    assert tuple(x for x in a) == ('a', 'b')

    # Extend non-empty list
    a = linkedlist.List(['a', 'b'])
    a.extend(['c', 'd'])
    assert len(a) == 4
    assert tuple(x for x in a) == ('a', 'b', 'c', 'd')


def test_list_insert():
    # Insert to empty list
    a = linkedlist.List()
    a.insert('a')
    assert len(a) == 1
    assert tuple(x for x in a) == ('a',)

    # Insert to non-empty list
    a = linkedlist.List([1, 2, 3])
    a.insert(0)
    assert len(a) == 4
    assert tuple(x for x in a) == (0, 1, 2, 3)


def test_list_popleft():
    # Pop from empty list should raise IndexError
    a = linkedlist.List()
    with pytest.raises(IndexError):
        a.popleft()

    # Pop from non-empty list should return first element.
    a = linkedlist.List(['a', 'b', 'c'])
    assert a.popleft() == 'a'
    assert len(a) == 2
    assert a.popleft() == 'b'
    assert len(a) == 1
    assert a.popleft() == 'c'
    assert len(a) == 0


def test_dlist_init():
    a = linkedlist.DoubleList()
    assert len(a) == 0

    a = linkedlist.DoubleList(['a', 'b'])
    assert len(a) == 2


def test_dlist_iter():
    a = linkedlist.DoubleList()
    assert tuple(x for x in a) == tuple()

    a = linkedlist.DoubleList(['a', 'b', 'c'])
    assert tuple(x for x in a) == ('a', 'b', 'c')


def test_dlist_append():
    a = linkedlist.DoubleList()
    a.append('a')
    assert tuple(x for x in a) == ('a',)
    assert len(a) == 1

    a.append('b')
    assert tuple(x for x in a) == ('a', 'b')
    assert len(a) == 2


def test_dlist_insert():
    a = linkedlist.DoubleList()
    # Insert with one argument should insert at the beginning of the list
    # ... when empty ...
    node = a.insert('a')
    assert isinstance(node, linkedlist.DoubleNode)
    assert tuple(x for x in a) == ('a',)
    assert len(a) == 1

    # ... or non-empty.
    node2 = a.insert('b')
    assert isinstance(node2, linkedlist.DoubleNode)
    assert tuple(x for x in a) == ('b', 'a')
    assert len(a) == 2

    # Insert with two arguments should insert before the target node.
    node3 = a.insert('c', node)
    assert isinstance(node3, linkedlist.DoubleNode)
    assert tuple(x for x in a) == ('b', 'c', 'a')
    assert len(a) == 3

    node4 = a.insert('d', node2)
    assert isinstance(node4, linkedlist.DoubleNode)
    assert tuple(x for x in a) == ('d', 'b', 'c', 'a')
    assert len(a) == 4


def test_dlist_pop():
    a = linkedlist.DoubleList(['a', 'b'])
    assert a.pop() == 'b'
    assert tuple(x for x in a) == ('a',)
    assert len(a) == 1

    assert a.pop() == 'a'
    assert tuple(x for x in a) == tuple()
    assert len(a) == 0


def test_dlist_remove():
    a = linkedlist.DoubleList(['a', 'b', 'c'])
    node = a.start.tail  # 'b'
    assert a.remove(node) == 'b'
    assert tuple(x for x in a) == ('a', 'c')
    assert len(a) == 2

    assert a.remove(a.start) == 'a'
    assert tuple(x for x in a) == ('c',)
    assert len(a) == 1

    assert a.remove(a.end) == 'c'
    assert tuple(x for x in a) == tuple()
    assert len(a) == 0
