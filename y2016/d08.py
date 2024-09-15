from PIL import Image


def parse(stream) -> list:
    results = []
    for line in stream:
        line = line.strip()
        words = line.split()
        command = words[0]
        match words[0]:
            case 'rect':
                ops = tuple(int(x) for x in words[1].split('x'))
            case 'rotate':
                row = words[1] == 'row'
                index = int(words[2].split('=')[1])
                count = int(words[-1])
                ops = (row, index, count)
        results.append((command, ops))
    return results


class Screen:
    def __init__(self, width: int = 50, height: int = 6):
        self.width = width
        self.height = height
        self.rows = []
        for _ in range(self.height):
            self.rows.append([0] * self.width)

    def draw_rect(self, width, height):
        for y in range(height):
            for x in range(width):
                self.rows[y][x] = 1

    def rotate_row(self, index, count):
        row = self.rows[index]
        self.rows[index] = row[-count:] + row[:-count]

    def rotate_column(self, index, count):
        col = [r[index] for r in self.rows]
        col = col[-count:] + col[:-count]
        for i, on in enumerate(col):
            self.rows[i][index] = on

    def draw(self) -> Image:
        pixel_size = 14
        height = (pixel_size + 1) * self.height + 1  # 1 pixel border
        width = (pixel_size + 1) * self.width + 1
        pixel = Image.open('assets/green_pixel_14.png')
        im = Image.new('RGB', (width, height), '#000')
        for i in range(self.height):
            for j in range(self.width):
                y = 1 + i * (pixel_size + 1)
                x = 1 + j * (pixel_size + 1)
                if self.rows[i][j]:
                    im.paste(pixel, (x, y))
        return im

    def run_instruction(self, instruction, operands):
        match instruction:
            case 'rect':
                w, h = operands
                self.draw_rect(w, h)
            case 'rotate':
                row, index, count = operands
                if row:
                    self.rotate_row(index, count)
                else:
                    self.rotate_column(index, count)

    def run_program(self, program: list):
        for inst, ops in program:
            self.run_instruction(inst, ops)

    def run_and_draw(self, program: list) -> list[Image]:
        images = []
        for inst, ops in program:
            self.run_instruction(inst, ops)
            images.append(self.draw())
        return images

    def count_on(self):
        return sum(sum(row) for row in self.rows)


def run(stream, test=False, draw=False):
    program = parse(stream)
    if test:
        size = 7, 3
    else:
        size = 50, 6
    screen = Screen(*size)

    if draw:
        images = screen.run_and_draw(program)
        images[0].save(
                'out/y2016d08.gif', save_all=True,
                append_images=images[1:], duration=300)
    else:
        screen.run_program(program)

    result1 = screen.count_on()
    result2 = 0
    return (result1, result2)
