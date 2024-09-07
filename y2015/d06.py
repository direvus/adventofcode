import re


PATTERN = re.compile(r'([\w ]+) (\d+),(\d+) through (\d+),(\d+)')


class Grid:
    def __init__(self, size=1000):
        self.size = size
        self.lights = [[0 for _ in range(size)] for _ in range(size)]

    def turn_on(self, y1: int, x1: int, y2: int, x2: int):
        chunk = [1] * (x2 - x1 + 1)
        for i in range(y1, y2 + 1):
            self.lights[i][x1:x2 + 1] = chunk

    def turn_off(self, y1: int, x1: int, y2: int, x2: int):
        chunk = [0] * (x2 - x1 + 1)
        for i in range(y1, y2 + 1):
            self.lights[i][x1:x2 + 1] = chunk

    def toggle(self, y1: int, x1: int, y2: int, x2: int):
        for i in range(y1, y2 + 1):
            chunk = [int(not x) for x in self.lights[i][x1:x2 + 1]]
            self.lights[i][x1:x2 + 1] = chunk

    def process_line(self, line: str) -> None:
        m = PATTERN.fullmatch(line)
        if not m:
            raise ValueError(f"Error: no match on {line}")
        cmd = m.group(1)
        x1 = int(m.group(2))
        y1 = int(m.group(3))
        x2 = int(m.group(4))
        y2 = int(m.group(5))
        match cmd:
            case 'turn off':
                self.turn_off(y1, x1, y2, x2)
            case 'turn on':
                self.turn_on(y1, x1, y2, x2)
            case 'toggle':
                self.toggle(y1, x1, y2, x2)
            case _:
                raise ValueError(f"Unknown instruction {cmd}")

    def count_lit(self):
        return sum(map(sum, self.lights))

    def to_image(self):
        from PIL import Image, ImageDraw
        size = 3 * self.size + 1  # 2 pixels per cell, plus border
        im = Image.new('RGB', (size, size), '#1a1a1a')
        draw = ImageDraw.Draw(im)
        for i in range(self.size):
            for j in range(self.size):
                y = 1 + i * 3
                x = 1 + j * 3
                if self.lights[i][j]:
                    draw.point([(x, y)], '#ffa126')
                    draw.point([(x + 1, y), (x, y + 1)], '#ffb737')
                    draw.point([(x + 1, y + 1)], '#ffca46')
        resize = im.resize((800, 800))
        resize.show()


def run(stream, test=False):
    result2 = 0
    grid = Grid()
    for line in stream:
        grid.process_line(line.strip())
    result1 = grid.count_lit()
    return (result1, result2)
