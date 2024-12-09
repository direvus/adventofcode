"""Advent of Code 2024

Day 9: Disk Fragmenter

https://adventofcode.com/2024/day/9
"""
import logging  # noqa: F401

from util import timing


class Node:
    def __init__(self, value, head=None, tail=None):
        self.value = value
        self.head = head
        self.tail = tail

    def __str__(self):
        return str(self.value)


class List:
    def __init__(self):
        self.start = None
        self.end = None
        self.space = 0
        self.index = []
        self.spacemap = []
        self.files = {}

    def append(self, value):
        node = Node(value, self.end)
        if self.start is None:
            self.start = node
        if self.end is not None:
            self.end.tail = node
        self.end = node
        if value is None:
            self.space += 1
        self.index.append(node)
        return node

    def pop(self):
        """Remove and return the last value of the list."""
        node = self.end
        self.end = node.head
        self.end.tail = None
        return node.value

    def __str__(self):
        node = self.start
        result = []
        while node is not None:
            result.append(str(node.value) if node.value is not None else '.')
            node = node.tail
        return ''.join(result)


def parse(stream) -> str:
    return tuple(map(int, stream.readline().strip()))


def make_list(values) -> Node:
    result = List()
    offset = 0
    for i, value in enumerate(values):
        blank = (i % 2 != 0)
        fileid = i // 2
        for _ in range(value):
            result.append(None if blank else fileid)
        if value > 0:
            if blank:
                result.spacemap.append((offset, value))
            else:
                result.files[fileid] = (offset, value)
        offset += value
    return result


def get_next_blank(node):
    while node is not None and node.value is not None:
        node = node.tail
    return node


def defrag(nodes: List):
    node = nodes.start
    space = nodes.space
    while space > 0:
        # Scan forward until we hit a blank node
        node = get_next_blank(node)
        value = nodes.pop()
        node.value = value
        space -= 1


def defrag_files(nodes: List):
    fileids = reversed(sorted(nodes.files.keys()))
    for fileid in fileids:
        offset, length = nodes.files[fileid]
        for i in range(len(nodes.spacemap)):
            space_offset, space_length = nodes.spacemap[i]
            if space_offset > offset:
                break
            if space_length >= length:
                for j in range(length):
                    nodes.index[space_offset + j].value = fileid
                    nodes.index[offset + j].value = None
                space_offset += length
                space_length -= length
                nodes.spacemap[i] = (space_offset, space_length)
                break


def get_checksum(nodes: List) -> int:
    node = nodes.start
    i = 0
    result = 0
    while node is not None:
        if node.value is not None:
            result += i * node.value
        node = node.tail
        i += 1
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        nodes = make_list(parsed)
        defrag(nodes)
        result1 = get_checksum(nodes)

    with timing("Part 2"):
        nodes = make_list(parsed)
        defrag_files(nodes)
        result2 = get_checksum(nodes)

    return (result1, result2)
