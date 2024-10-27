"""Advent of Code 2021

Day 16: Packet Decoder

https://adventofcode.com/2021/day/16
"""
import logging  # noqa: F401
from math import ceil

from util import timing


HEX_TO_BIN = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
        }


class Packet:
    def __init__(self, version, typeid):
        self.version = version
        self.typeid = typeid
        self.value = None
        self.packets = []

    def get_total_versions(self) -> int:
        """Return the sum of versions of this and all descendant packets."""
        result = self.version
        for subpacket in self.packets:
            result += subpacket.get_total_versions()
        return result


class Message:
    def __init__(self, hexstring: str):
        self.hex = hexstring
        self.pointer = 0
        self.buffer = ''

    def get_bits(self, count: int) -> str:
        """Return `count` bits of data from the stream.

        The return is a text string consisting of ones and zeroes. If there is
        not enough data on the stream to deliver `count` bits, raise a
        ValueError.
        """
        # First try to pull the bits from the internal buffer.
        if len(self.buffer) >= count:
            result = self.buffer[:count]
            self.buffer = self.buffer[count:]
            return result

        # If we're still here, then the internal buffer did not satisfy the
        # request. Try translating some hex digits into bits.
        required = ceil((count - len(self.buffer)) / 4)
        avail = len(self.hex) - self.pointer
        if avail < required:
            raise ValueError(
                    f'Need {required} hex digits, but only {avail} remain')

        hexes = self.hex[self.pointer: self.pointer + required]
        self.pointer += required
        for h in hexes:
            self.buffer += HEX_TO_BIN[h]

        result = self.buffer[:count]
        self.buffer = self.buffer[count:]
        return result

    def get_int(self, bitcount: int) -> int:
        """Get some bits and convert to an integer."""
        return int(self.get_bits(bitcount), 2)

    def get_literal(self) -> int:
        """Get a literal integer value from a type 4 packet.

        Literals are encoded in a series of 5-bit chunks, where the first bit
        of each chunk is a continuation marker, and the remaining 4 bits are
        the data.
        """
        stop = False
        data = []
        while not stop:
            chunk = self.get_bits(5)
            data.append(chunk[1:])
            if chunk[0] == '0':
                stop = True
        return int(''.join(data), 2)

    def decode_packet(self):
        version = self.get_int(3)
        typeid = self.get_int(3)
        packet = Packet(version, typeid)
        if typeid == 4:
            packet.value = self.get_literal()
            return packet

        # It's an operator packet
        lentype = self.get_bits(1)
        if lentype == '0':
            # Length is number of bits -- keep reading in packets until we have
            # read that at least that many bits.
            length = self.get_int(15)
            required = ceil((length - len(self.buffer)) / 4)
            end = self.pointer + required
            while self.pointer < end:
                subpacket = self.decode_packet()
                packet.packets.append(subpacket)
        else:
            # Length is number of immediate sub-packets
            length = self.get_int(11)
            while len(packet.packets) < length:
                subpacket = self.decode_packet()
                packet.packets.append(subpacket)
        return packet


def parse(stream) -> Message:
    line = stream.readline().strip()
    return Message(line)


def run(stream, test: bool = False):
    with timing("Part 1"):
        message = parse(stream)
        packet = message.decode_packet()
        result1 = packet.get_total_versions()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
