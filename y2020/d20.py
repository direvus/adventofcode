"""Advent of Code 2020

Day 20: Jurassic Jigsaw

https://adventofcode.com/2020/day/20
"""
import logging  # noqa: F401
from collections import deque
from math import prod

from util import timing


ORIENTATIONS = (
        'original',
        'left',  # rotate counter-clockwise 90 degrees
        'half',  # rotate 180 degrees
        'right',  # rotate clockwise 90 degrees
        'vertical',  # flip vertically
        'horizontal',  # flip horizontally
        'horizontal-left',  # flip horizontally then rotate left
        'vertical-left',  # flip vertically then rotate left
        )
EDGE_ORIENTATIONS = (
        (0, 1, 2, 3),
        (1, 6, 3, 4),
        (6, 7, 4, 5),
        (7, 0, 5, 2),
        (2, 5, 0, 7),
        (4, 3, 6, 1),
        (3, 2, 1, 0),
        (5, 4, 7, 6),
        )
PATTERN = {
        #                   #
        # #    ##    ##    ###
        #  #  #  #  #  #  #
        (18, 0),
        (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1),
        (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2)}



class Tile:
    def __init__(self, name: int, stream, size: int = 10):
        self.name = name
        self.size = size
        self.pixels = set()
        self._edges = set()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        for line in stream:
            line = line.strip()
            if line == '':
                break
            for x, ch in enumerate(line):
                if ch == '#':
                    self.pixels.add((x, y))
            y += 1

    def __str__(self) -> str:
        lines = []
        for y in range(self.size):
            line = []
            for x in range(self.size):
                ch = '#' if (x, y) in self.pixels else '.'
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)

    @property
    def edges(self) -> set:
        if self._edges:
            return self._edges

        top = []
        bottom = []
        left = []
        right = []
        for i in range(self.size):
            top.append(int((i, 0) in self.pixels))
            bottom.append(int((i, self.size - 1) in self.pixels))
            left.append(int((0, i) in self.pixels))
            right.append(int((self.size - 1, i) in self.pixels))

        result = [
                tuple(top),
                tuple(right),
                tuple(bottom),
                tuple(left),
                tuple(reversed(top)),
                tuple(reversed(right)),
                tuple(reversed(bottom)),
                tuple(reversed(left)),
                ]
        self._edges = result
        return result

    def get_edge(self, edge: int, orientation: int) -> tuple:
        """Return an edge from this tile under the given orientation.

        `edge` should be the edge number, counting from zero at the top edge
        and working around clockwise.

        `orientation` should be an integer from 0-7, indicating one of the
        eight possible indexes into `ORIENTATIONS`.

        The result is a tuple of ones and zeroes, where ones indicate active
        pixels.
        """
        edges = self.edges
        index = EDGE_ORIENTATIONS[orientation][edge]
        return edges[index]

    def transform_position(self, position: tuple, orientation: int) -> tuple:
        x, y = position
        match orientation:
            case 0:
                return position
            case 1:
                # Rotate 90 degrees counter-clockwise
                return (y, self.size - x - 1)
            case 2:
                # Rotate 180 degrees
                return (self.size - y - 1, self.size - x - 1)
            case 3:
                # Rotate 90 degrees clockwise
                return (self.size - y - 1, x)
            case 4:
                # Flip vertically
                return (x, self.size - y - 1)
            case 5:
                # Flip horizontally
                return (self.size - x - 1, y)
            case 6:
                # Flip horizontally and rotate 90 degrees left
                flip = self.transform_position(position, 5)
                return self.transform_position(flip, 1)
            case 7:
                # Flip vertically and rotate 90 degrees left
                flip = self.transform_position(position, 4)
                return self.transform_position(flip, 1)

    def transform(self, orientation: int):
        """Return a new Tile in the given orientation."""
        result = Tile(f'{self.name}-{orientation}', '', self.size)
        for y in range(self.size):
            for x in range(self.size):
                p = (x, y)
                if p in self.pixels:
                    t = self.transform_position(p, orientation)
                    result.pixels.add(t)
        return result

    def find_pattern(self, pattern: set, height: int, width: int) -> set:
        """Look for a particular pattern in this tile.

        Look for positions where the given pattern of pixels appears. Return
        the set of coordinates where the top left corner of the pattern
        matches.
        """
        result = set()
        for y in range(self.size - height + 1):
            for x in range(self.size - width + 1):
                valid = True
                for px, py in pattern:
                    if (px + x, py + y) not in self.pixels:
                        valid = False
                        break
                if valid:
                    result.add((x, y))
        return result


class TileSet:
    def __init__(self, stream, tilesize: int = 10):
        self.tiles = {}
        self.size = None
        self.tilesize = tilesize
        if stream:
            self.parse(stream)

    def parse(self, stream):
        line = stream.readline().strip()
        while line.startswith('Tile'):
            name = int(line[:-1].split()[1])
            tile = Tile(name, stream)
            self.tiles[name] = tile
            # The Tile parser should have advanced the stream to the next
            # "Tile" line.
            line = stream.readline().strip()
        self.size = int(len(self.tiles) ** 0.5)

    def get_common_edges(self, tile: int) -> set[int]:
        """Return the edges of `tile` that match any other tile."""
        edges = set(self.tiles[tile].edges)
        result = set()
        for other in self.tiles:
            if other == tile:
                continue
            matched = edges & set(self.tiles[other].edges)
            edges -= matched
            result |= matched
            if not edges:
                # All edges have matched, no need to keep going
                break
        return result

    def count_common_edges(self, tile: int) -> int:
        """Return the number of edges of `tile` that match another tile."""
        return len(self.get_common_edges(tile))

    def find_corners(self) -> set[int]:
        """Find the tiles that must be in the corners of the mosaic.

        We find the corner tiles by counting the number of edges on each tile
        that can possibly match to some other tile. If there are 2 edges with
        no possible match to another tile, then the tile has to go on a corner.
        """
        result = set()
        for name in self.tiles:
            count = self.count_common_edges(name)
            if count <= 4:
                result.add(name)
        return result

    def get_first_tile(self, tiles: dict) -> tuple | None:
        """Return the first empty tile in reading order.

        Return the position of the first empty tile in a mosaic configuration,
        or None if all tiles are populated.
        """
        for y in range(self.size):
            for x in range(self.size):
                p = (x, y)
                if p not in tiles:
                    return p
        return None

    def find_fits(self, mosaic: dict, position: tuple, tile: int):
        """Return all the ways that the tile could fit in this position.

        If the tile cannot fit into this position (its edges are not compatible
        with the adjacent tiles in any rotation) then return the empty set.

        Otherwise, return a set of the valid rotations for the tile.
        """
        result = set()
        x, y = position
        # This ordering is carefully arranged so that the index corresponds to
        # the adjacent edge (0 = top, increasing clockwise) of the other tile.
        coords = ((x, y + 1), (x - 1, y), (x, y - 1), (x + 1, y))
        adjacents = {}
        for i, p in enumerate(coords):
            if p not in mosaic:
                continue
            t, o = mosaic[p]
            edge = self.tiles[t].get_edge(i, o)
            adjacents[(i + 2) % 4] = edge

        for orientation in range(8):
            valid = True
            for index, adj in adjacents.items():
                edge = self.tiles[tile].get_edge(index, orientation)
                if edge != adj:
                    valid = False
                    break
            if valid:
                result.add(orientation)
        return result

    def find_mosaics(self, corners):
        """Find the ways that these tiles can be assembled into a mosaic.

        Return each of the possible configurations as a dict mapping tile
        coordinates to tile names.
        """
        maximum = self.size - 1
        # Pick any arbitrary corner tile to be in the top-left.
        topleft = next(iter(corners))

        # Find a way to orient the top-left tile so that its common
        # edges face the interior. There will actually be two ways this works,
        # but they will yield rotationally equivalent outcomes, so just pick
        # the first one.
        tile = self.tiles[topleft]
        common = self.get_common_edges(topleft)
        candidates = []
        for i in range(len(ORIENTATIONS)):
            right = tile.get_edge(1, i)
            bottom = tile.get_edge(2, i)
            if right in common and bottom in common:
                config = {(0, 0): (topleft, i)}
                candidates.append(config)
                break

        # Set up the configurations with each other corner tile selected into
        # the bottom-right position. It doesn't matter how the other two
        # corner tiles are arranged into the top-right and bottom-left.
        p = (maximum, maximum)
        new = []
        for corner in corners:
            if corner == topleft:
                continue
            tile = self.tiles[corner]
            common = self.get_common_edges(corner)
            for candidate in candidates:
                for i in range(len(ORIENTATIONS)):
                    config = dict(candidate)
                    top = tile.get_edge(0, i)
                    left = tile.get_edge(3, i)
                    if top in common and left in common:
                        config[p] = (corner, i)
                        new.append(config)
        candidates = new

        # Considering each of the open positions in reading order, for each of
        # the candidate configurations, look through the pool of remaining
        # tiles for those that can possibly fit into the position, and produce
        # new configurations for all the ways it can fit.
        results = []
        q = deque(candidates)
        while q:
            config = q.popleft()
            p = self.get_first_tile(config)
            if p is None:
                # This config is fully populated, add it to the final results.
                results.append(config)
                continue

            placed = {x[0] for x in config.values()}
            pool = set(self.tiles.keys()) - placed
            for tile in pool:
                for fit in self.find_fits(config, p, tile):
                    new = dict(config)
                    new[p] = (tile, fit)
                    q.append(new)
        return results

    def assemble(self):
        """Find a way to assemble the images into a mosaic.

        Individual tiles may be flipped or rotated in any way to make them fit,
        and edges must align between adjacent tiles.

        The result is a single Tile object with all edge pixels removed.
        """
        size = self.size
        # This better be a perfect square, or we are out of luck
        assert size ** 2 == len(self.tiles)

        corners = self.find_corners()

        # Okay now we can attempt to connect these tiles together into a
        # complete mosaic. There should really only be one valid solution but
        # as long as there's at least one, we'll take it.
        candidates = self.find_mosaics(corners)
        if len(candidates) == 0:
            raise ValueError("No solution found for mosaic!")
        mosaic = candidates[0]

        # Now we need to stitch these tiles together into one jumbo tile, while
        # omitting their borders.
        internalsize = self.tilesize - 2
        resultsize = internalsize * self.size
        result = Tile(0, '', resultsize)
        for y in range(self.size):
            for x in range(self.size):
                name, orientation = mosaic[(x, y)]
                tile = self.tiles[name]
                tile = tile.transform(orientation)
                for ty in range(1, self.tilesize - 1):
                    for tx in range(1, self.tilesize - 1):
                        if (tx, ty) in tile.pixels:
                            px = x * internalsize + tx - 1
                            py = y * internalsize + ty - 1
                            result.pixels.add((px, py))
        return result


def parse(stream) -> TileSet:
    return TileSet(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        tiles = parse(stream)
        corners = tiles.find_corners()
        if len(corners) != 4:
            raise ValueError(f"found {len(corners)} corner tiles!")
        result1 = prod(corners)

    with timing("Part 2"):
        mosaic = tiles.assemble()
        for i in range(8):
            tile = mosaic.transform(i)
            hits = tile.find_pattern(PATTERN, 3, 20)
            pixels = set(tile.pixels)
            if hits:
                for x, y in hits:
                    pixels -= {(px + x, py + y) for px, py in PATTERN}
                result2 = len(pixels)
                break

    return (result1, result2)
