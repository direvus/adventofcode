from PIL import Image

import visualise


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

    def draw(self, animation, pixel, sprites, time):
        for i in range(self.height):
            for j in range(self.width):
                if self.rows[i][j] and (j, i) not in sprites:
                    x = 1 + (pixel.size[0] + 1) * j
                    y = 1 + (pixel.size[1] + 1) * i
                    sprite = visualise.Sprite(
                            pixel, (x, y),
                            start=time, fade_in=4, fade_out=4)
                    animation.add_element(sprite)
                    sprites[(j, i)] = sprite
                elif not self.rows[i][j] and (j, i) in sprites:
                    sprite = sprites[(j, i)]
                    sprite.stop = time - 1
                    del sprites[(j, i)]

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

    def run_and_draw(self, program: list):
        pixel_size = 14
        image_size = (
                (pixel_size + 1) * self.width + 1,
                (pixel_size + 1) * self.height + 1,
                )
        pixel = Image.open('assets/green_pixel_14.png')
        anim = visualise.Animation(image_size, 24, '#000')
        sprites = {}
        rate = 12  # frames per update
        t = 0

        for inst, ops in program:
            self.run_instruction(inst, ops)
            self.draw(anim, pixel, sprites, t)
            t += rate
        anim.render('out/y2016d08.gif', stop=t - 1)

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
        screen.run_and_draw(program)
    else:
        screen.run_program(program)

    result1 = screen.count_on()
    result2 = 0
    return (result1, result2)
