"""visualise.py

Utility module for building animated visualisations.
"""
import bisect
import logging  # noqa: F401
from collections import OrderedDict
from enum import Enum
from operator import add

from PIL import Image

from util import INF


def ease_cubic_out(time: float) -> float:
    return 1 - ((1 - time) ** 3)


def ease_cubic_in(time: float) -> float:
    return 1 - (time ** 3)


def ease_cubic_in_out(x):
    if x < 0.5:
        return 4 * (x ** 3)
    else:
        return 1 - ((x * -2 + 2) ** 3) / 2


class Status(Enum):
    ACTIVE = 0
    EXTINCT = 1
    PERMANENT = 2


class Element:
    def render(self, canvas, time):
        raise NotImplementedError()


class Sprite(Element):
    final_status = Status.EXTINCT

    def __init__(
            self, image, position=None, start=None, stop=None,
            final_status=None, fade_in=None, fade_out=None):
        if isinstance(image, Image.Image):
            self.image = image
        else:
            self.image = Image.open(image)
        self.position = position
        self.start = start
        self.stop = stop
        if final_status is not None:
            self.final_status = final_status
        self.fades = OrderedDict()
        self.movements = OrderedDict()
        self.fade_in = fade_in
        self.fade_out = fade_out

    def add_fade(self, start, duration, initial, final, easing=None):
        transition = (start, duration, initial, final, easing)
        self.fades[start] = transition
        return transition

    def add_movement(self, start, duration, origin, vector, easing=None):
        if easing is None:
            easing = ease_cubic_in_out
        transition = (start, duration, origin, vector, easing)
        self.movements[start] = transition
        return transition

    def get_coordinates(self, position):
        """Translate a position into image pixel coordinates.

        By default, no translation is performed and the position is returned
        as-is.

        Override this method when the sprite position is in a different
        coordinate system than the image canvas.
        """
        return position

    def get_position(self, canvas, time):
        keys = list(self.movements.keys())
        key = bisect.bisect_right(keys, time)
        if not key:
            return self.get_coordinates(self.position)
        index = keys[key - 1]
        start, duration, source, vector, easing = self.movements[index]
        end = start + duration
        if end <= time:
            # The latest movement has completed at this `time`, so return its
            # final position.
            dest = tuple(map(add, source, vector))
            coords = self.get_coordinates(dest)
            return coords
        progress = (time - start) / duration
        value = easing(progress)
        scaledvector = (v * value for v in vector)
        position = map(add, source, scaledvector)
        coords = self.get_coordinates(position)
        result = tuple(map(round, coords))
        return result

    def get_alpha(self, time):
        if (
                self.fade_in is not None and
                self.start is not None and
                time <= self.start + self.fade_in):
            offset = (time - self.start) / self.fade_in
            return ease_cubic_out(offset)

        if (
                self.fade_out is not None and
                self.stop is not None and
                time >= self.stop - self.fade_out):
            start = self.stop - self.fade_out
            offset = (time - start) / self.fade_out
            return ease_cubic_in(offset)

        keys = list(self.fades.keys())
        key = bisect.bisect_right(keys, time)
        if not key:
            return None
        index = keys[key - 1]
        start, duration, initial, final, easing = self.fades[index]
        end = start + duration
        if end <= time:
            # The latest fade has completed at this `time`, so return its
            # final value.
            return final

        progress = (time - start) / duration
        scale = easing(progress)
        diff = (final - initial) * scale
        value = start + diff
        return value

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
        if alpha is None and not self.image.has_transparency_data:
            canvas.paste(self.image, position)
            return status

        if alpha is None:
            alpha = 1.0
        if not self.image.has_transparency_data:
            # Just apply the transparency as a static value to the entire image
            self.image.putalpha(round(255 * alpha))
            canvas.alpha_composite(self.image, position)
            return status

        # If we've arrived here, then the sprite has its own transparency
        # channel, which we need to scale according to the alpha value to get
        # the new alpha channel.  This will only work with images that have a
        # channel named 'A', so pretty much only 'RGBA' or 'LA' image modes.
        mask = self.image.getchannel('A')
        data = list(mask.getdata())
        data = [round(alpha * x) for x in data]

        temp = self.image.copy()  # Avoid modifying the original sprite
        mask.putdata(data)
        temp.putalpha(mask)
        canvas.alpha_composite(temp, position)
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
