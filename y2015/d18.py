from PIL import Image, ImageDraw


class Grid:
    """A square grid of binary light cells"""
    def __init__(self):
        self.lights = []
        self.size = None

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            self.lights.append([int(x == '#') for x in line])
        self.size = len(self.lights)

    def count_on(self):
        return sum(map(sum, self.lights))

    def count_on_neighbours(self, row: int, col: int) -> int:
        result = 0
        for i in range(max(0, row - 1), min(self.size, row + 2)):
            result += sum(self.lights[i][max(0, col - 1): col + 2])
        return result

    def update(self):
        new = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                v = self.lights[i][j]
                n = self.count_on_neighbours(i, j) - v
                if v:
                    v = int(n in {2, 3})
                else:
                    v = int(n == 3)
                row.append(v)
            new.append(row)
        self.lights = new

    def run(self, steps: int):
        for _ in range(steps):
            self.update()

    def draw(self) -> Image:
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
        return im

    def run_and_draw(self, steps: int) -> list[Image]:
        images = []
        for _ in range(steps):
            self.update()
            images.append(self.draw())
        return images


class CornerLockedGrid(Grid):
    @property
    def corners(self) -> set:
        m = self.size - 1
        return {(0, 0), (0, m), (m, 0), (m, m)}

    def update(self):
        new = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) in self.corners:
                    v = 1
                else:
                    v = self.lights[i][j]
                    n = self.count_on_neighbours(i, j) - v
                    if v:
                        v = int(n in {2, 3})
                    else:
                        v = int(n == 3)
                row.append(v)
            new.append(row)
        self.lights = new

    def setup_corners(self):
        for i, j in self.corners:
            self.lights[i][j] = 1

    def run(self, steps: int):
        self.setup_corners()
        super().run(steps)

    def run_and_draw(self, steps: int):
        self.setup_corners()
        return super().run_and_draw(steps)


def run(stream, test=False, draw=False):
    steps = 4 if test else 100
    grid = Grid()
    grid.parse(stream)
    grid2 = CornerLockedGrid()
    grid2.lights = grid.lights
    grid2.size = grid.size
    if draw:
        images = grid.run_and_draw(steps)
        images[0].save(
                'out/y2015d18p1.gif', save_all=True,
                append_images=images[1:], duration=200)
    else:
        grid.run(steps)

    result1 = grid.count_on()

    if test:
        steps = 5

    if draw:
        images = grid2.run_and_draw(steps)
        images[0].save(
                'out/y2015d18p2.gif', save_all=True,
                append_images=images[1:], duration=200)
    else:
        grid2.run(steps)
    result2 = grid2.count_on()
    return (result1, result2)
