"""visualise.py

Utility module for building animated visualisations.
"""
import bisect
import logging  # noqa: F401
from collections import OrderedDict
from enum import Enum
from operator import add, sub

from PIL import Image, ImageDraw, ImageFont

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
    """Abstract base class for an animated element.

    The base class handles things like positioning and transition logic. The
    details about how to render an Element on to a canvas is left up to
    inheriting classes to determine.
    """
    final_status = Status.EXTINCT

    def __init__(
            self, position=None, start=None, stop=None,
            final_status=None, fade_in=None, fade_out=None):
        self.position = position
        self.start = start
        self.stop = stop
        if final_status is not None:
            self.final_status = final_status
        self.fades = OrderedDict()
        self.movements = OrderedDict()
        self.crops = OrderedDict()
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

    def add_crop(self, start, duration, initial, final, easing=None):
        if easing is None:
            easing = ease_cubic_in_out
        transition = (start, duration, initial, final, easing)
        self.crops[start] = transition
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

    def get_crop(self, time):
        """Return the crop box, or None if no crop should apply.

        The default behaviour is to do no cropping, unless crop transitions are
        in effect.
        """
        keys = list(self.crops.keys())
        key = bisect.bisect_right(keys, time)
        if not key:
            return None

        index = keys[key - 1]
        start, duration, initial, final, easing = self.crops[index]
        end = start + duration
        if end <= time:
            # The latest transition has completed at this `time`, so return its
            # final crop box.
            coords = self.get_coordinates(final)
            return coords
        progress = (time - start) / duration
        value = easing(progress)

        vector = map(sub, final, initial)
        scaledvector = (v * value for v in vector)
        box = map(add, initial, scaledvector)
        coords = self.get_coordinates(box)
        result = tuple(map(round, coords))
        return result

    def render(self, canvas, time):
        raise NotImplementedError()


class Sprite(Element):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(image, Image.Image):
            self.image = image
        else:
            self.image = Image.open(image)

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
        image = self.image.copy()  # Avoid modifying the original sprite
        crop = self.get_crop(time)
        if crop is not None:
            image = image.crop(crop)
            left, top = crop[:2]
            x, y = position
            position = (x + left, y + top)

        alpha = self.get_alpha(time)
        if alpha is None and not image.has_transparency_data:
            canvas.paste(image, position)
            return status

        if alpha is None:
            alpha = 1.0
        if not image.has_transparency_data:
            # Just apply the transparency as a static value to the entire image
            image.putalpha(round(255 * alpha))
            canvas.alpha_composite(image, position)
            return status

        # If we've arrived here, then the sprite has its own transparency
        # channel, which we need to scale according to the alpha value to get
        # the new alpha channel.  This will only work with images that have a
        # channel named 'A', so pretty much only 'RGBA' or 'LA' image modes.
        mask = image.getchannel('A')
        data = list(mask.getdata())
        data = [round(alpha * x) for x in data]

        mask.putdata(data)
        image.putalpha(mask)
        canvas.alpha_composite(image, position)
        return status


class Text(Element):
    def __init__(
            self, font, size, text='', colour='#ffffff', align='left',
            spacing=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(font, str):
            self.font = ImageFont.truetype(font)
        else:
            self.font = font
        self.font = font
        self.size = size
        self.text = text
        self.colour = colour
        self.align = align
        self.spacing = spacing

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

        image = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(image)
        draw.text(
                xy=(0, 0),
                text=self.text,
                fill=self.colour,
                font=self.font,
                align=self.align,
                spacing=self.spacing)

        crop = self.get_crop(time)
        if crop is not None:
            image = image.crop(crop)

        position = self.get_position(canvas, time)
        alpha = self.get_alpha(time)

        if alpha is None:
            alpha = 1.0

        mask = image.getchannel('A')
        data = list(mask.getdata())
        data = [round(alpha * x) for x in data]

        mask.putdata(data)
        image.putalpha(mask)
        canvas.alpha_composite(image, position)
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

    def add_elements(self, *args):
        for arg in args:
            self.elements.append(arg)

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
