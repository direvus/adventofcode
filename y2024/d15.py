"""Advent of Code 2024

Day 15: Warehouse Woes

https://adventofcode.com/2024/day/15
"""
import bisect
import logging  # noqa: F401
from collections import deque, OrderedDict
from operator import add

from PIL import Image

from util import timing
import grid
import visualise


def get_coords(position):
    return tuple(map(lambda v: 1 + 5 * v, position))


class Sprite(visualise.Sprite):
    def __init__(self, *args, **kwargs):
        self.transitions = OrderedDict()
        kwargs['final_status'] = visualise.Status.PERMANENT
        super().__init__(*args, **kwargs)

    def add_transition(self, start, duration, source, vector):
        self.transitions[start] = (start, duration, source, vector)
        self.stop = start + duration

    def get_position(self, canvas, time):
        keys = list(self.transitions.keys())
        key = bisect.bisect_right(keys, time)
        if not key:
            return get_coords(self.position)
        index = keys[key - 1]
        start, duration, source, vector = self.transitions[index]
        end = start + duration
        if end <= time:
            # It's already completed
            dest = tuple(map(add, source, vector))
            coords = get_coords(dest)
            return coords
        progress = (time - start) / duration
        easing = visualise.ease_cubic_in_out(progress)
        vector = map(lambda v: v * easing, vector)
        position = map(add, source, vector)
        coords = get_coords(position)
        result = tuple(map(round, coords))
        return result


class Grid(grid.SparseGrid):
    def __init__(self):
        super().__init__()
        self.walls = set()
        self.boxes = {}
        self.start = None
        self.robot_sprite = None
        self.box_sprites = {}

    def parse_cell(self, position: tuple, value: str | int):
        if value == '#':
            self.walls.add(position)
        elif value == 'O':
            self.boxes[len(self.boxes)] = position
        elif value == '@':
            self.start = position

    def do_move(
            self, position, direction: int,
            draw: bool = False, time: int | None = None):
        boxes = set()
        box_positions = {v: k for k, v in self.boxes.items()}
        ahead = position
        while True:
            ahead = grid.move(ahead, direction)
            if ahead in box_positions:
                boxes.add(box_positions[ahead])
            elif ahead in self.walls:
                # Move not possible
                return position
            else:
                break
        # Relocate all the boxes that are getting pushed.
        for box in boxes:
            source = self.boxes[box]
            dest = grid.move(self.boxes[box], direction)
            self.boxes[box] = dest
            if draw:
                self.box_sprites[box].add_transition(
                        time, 6, source, grid.VECTORS[direction])
        if draw:
            self.robot_sprite.add_transition(
                    time, 6, position, grid.VECTORS[direction])
        result = grid.move(position, direction)
        return result

    def do_moves(self, moves, draw: bool = False):
        anim = None
        time = 0
        lead = 12
        rate = 4  # frames per movement round
        if draw:
            wall = Image.open('assets/grey_pixel_4.png')
            box = Image.open('assets/white_pixel_4.png')

            grid_size = (self.width, self.height)
            size = get_coords(grid_size)
            anim = visualise.Animation(size, 24, '#1a1a1a')

            for p in self.walls:
                sprite = visualise.Sprite(
                        wall, get_coords(p), stop=lead, fade_in=lead,
                        final_status=visualise.Status.PERMANENT)
                anim.add_element(sprite)
            self.robot_sprite = Sprite(
                    'assets/gold_pixel_4.png', self.start,
                    fade_in=lead)
            anim.add_element(self.robot_sprite)
            self.box_sprites = {}
            for i, p in self.boxes.items():
                sprite = Sprite(box, p, fade_in=lead)
                self.box_sprites[i] = sprite
                anim.add_element(sprite)
            time += lead

        position = self.start
        for move in moves:
            position = self.do_move(position, move, draw, time)
            time += rate

        if draw:
            anim.render('out/y2024d15p1.gif', 0, min(time, 3000))

    def get_total_box_score(self):
        return sum(map(get_box_score, self.boxes.values()))

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                ch = (
                        '#' if p in self.walls else
                        'O' if p in self.boxes else
                        '.')
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


class WideGrid(Grid):
    def parse_cell(self, position: tuple, value: str | int):
        x, y = position
        x *= 2
        position = (x, y)
        if value == '#':
            self.walls.add(position)
            self.walls.add((x + 1, y))
        elif value == 'O':
            self.boxes[len(self.boxes)] = position
        elif value == '@':
            self.start = position

    def parse(self, stream):
        super().parse(stream)
        self.width *= 2
        return self

    def do_move(
            self, position, direction: int,
            draw: bool = False, time: int | None = None):
        boxes = set()
        box_positions = {}
        for i, p in self.boxes.items():
            box_positions[p] = i
            box_positions[(p[0] + 1, p[1])] = i

        q = deque()
        q.append(position)
        visited = set()
        while q:
            p = q.popleft()
            ahead = grid.move(p, direction)
            if ahead in self.walls:
                # Move not possible
                return position

            if ahead in visited:
                continue

            if ahead in box_positions:
                index = box_positions[ahead]
                box = self.boxes[index]
                side = (box[0] + 1, box[1])
                boxes.add(index)
                q.append(box)
                q.append(side)
                visited |= {box, side}

        # Relocate all boxes that are getting pushed
        for box in boxes:
            p = grid.move(self.boxes[box], direction)
            self.boxes[box] = p
        return grid.move(position, direction)

    def __str__(self):
        lines = []
        boxes = set(self.boxes.values())
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                ch = (
                        '#' if p in self.walls else
                        '[' if p in boxes else
                        ']' if (x - 1, y) in boxes else
                        '.')
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> str:
    data = stream.read()
    plan, moves = data.split('\n\n')
    plan = plan.split('\n')
    moves = ''.join(moves.split())
    moves = tuple(map(lambda x: grid.FACING.index(x), moves.strip()))
    return plan, moves


def get_box_score(position) -> int:
    return position[0] + (position[1] * 100)


def run(stream, test: bool = False, draw: bool = False):
    with timing("Part 1"):
        plan, moves = parse(stream)
        grid = Grid().parse(plan)
        grid.do_moves(moves, draw)
        result1 = grid.get_total_box_score()

    with timing("Part 2"):
        wide = WideGrid().parse(plan)
        wide.do_moves(moves)
        result2 = wide.get_total_box_score()

    return (result1, result2)