"""visualise.py

Utility module for building animated visualisations.
"""
from enum import Enum

from PIL import Image

from util import INF


class Status(Enum):
    ACTIVE = 0
    EXTINCT = 1
    PERMANENT = 2


class Element:
    def render(self, canvas, time):
        raise NotImplementedError()


class Sprite(Element):
    def __init__(
            self, image, position=None, start=None, stop=None,
            final_status=Status.EXTINCT, fade_in=None, fade_out=None):
        if isinstance(image, Image.Image):
            self.image = image
        else:
            self.image = Image.open(image)
        self.position = position
        self.start = start
        self.stop = stop
        self.final_status = final_status
        self.fade_in = fade_in
        self.fade_out = fade_out

    def get_position(self, canvas, time):
        return self.position

    def get_fade_in_alpha(self, time: float) -> float:
        # Default to a cubic ease-out
        return 1 - ((1 - time) ** 3)

    def get_fade_out_alpha(self, time: float) -> float:
        # Default to a cubic ease-in
        return 1 - (time ** 3)

    def get_alpha(self, time):
        if (
                self.fade_in is not None and
                self.start is not None and
                time <= self.start + self.fade_in):
            offset = (time - self.start) / self.fade_in
            return round(255 * self.get_fade_in_alpha(offset))

        if (
                self.fade_out is not None and
                self.stop is not None and
                time >= self.stop - self.fade_out):
            start = self.stop - self.fade_out
            offset = (time - start) / self.fade_out
            return round(255 * self.get_fade_out_alpha(offset))

        return None

    def render(self, canvas, time) -> Status:
        status = Status.ACTIVE
        if self.start is not None and time < self.start:
            # Not ready to be displayed yet
            return status

        if self.stop is not None and time > self.stop:
            # Finished displaying
            status = self.final_status
            if status == Status.EXTINCT:
                return status

        position = self.get_position(canvas, time)
        alpha = self.get_alpha(time)
        if alpha is None:
            canvas.paste(self.image, position)
        else:
            self.image.putalpha(alpha)
            canvas.alpha_composite(self.image, position)
        return status


class Animation:
    def __init__(self, size, rate, background):
        self.width, self.height = size
        self.rate = rate
        self.elements = []

        if isinstance(background, Image.Image):
            self.background = background
        else:
            self.background = Image.new('RGBA', size, background)

    def add_element(self, element):
        self.elements.append(element)
        return element

    def render_frame(self, time):
        im = self.background.copy()
        delete = set()
        for i, element in enumerate(self.elements):
            status = element.render(im, time)
            if status == Status.EXTINCT:
                delete.add(i)
            elif status == Status.PERMANENT:
                element.render(self.background, time)
                delete.add(i)

        if delete:
            self.elements = [
                    x for i, x in enumerate(self.elements)
                    if i not in delete]
        return im

    def render(self, filename: str, start: int = 0, stop: int = INF):
        frames = []
        t = start
        while self.elements and t <= stop:
            frame = self.render_frame(t)
            frames.append(frame)
            t += 1
        initial = frames[0]
        duration = 1000 / self.rate  # milliseconds
        initial.save(
                filename, save_all=True, append_images=frames[1:],
                duration=duration)
        return initial
