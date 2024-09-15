import math
import re
from collections import defaultdict


MARKER = re.compile(r'\((\d+)x(\d+)\)')


class Bot:
    def __init__(self, low=None, high=None):
        self.low = low
        self.high = high
        self.chips = []

    def append(self, chip: int):
        self.chips.append(chip)

    def __len__(self) -> int:
        return len(self.chips)

    def get_sorted_chips(self) -> tuple:
        return tuple(sorted(self.chips))

    def clear(self):
        self.chips = []


class Factory:
    def __init__(self):
        self.inputs = {}
        self.bots = defaultdict(lambda: Bot())
        self.outputs = defaultdict(list)

    def get_collection(self, typ: str):
        if typ == 'bot':
            return self.bots
        else:
            return self.outputs

    def parse(self, stream) -> str:
        for line in stream:
            line = line.strip()
            words = line.split()
            match words[0]:
                case 'value':
                    value = int(words[1])
                    target = int(words[-1])
                    self.inputs[value] = self.bots[target]
                case 'bot':
                    bot = self.bots[int(words[1])]
                    bot.low = self.get_collection(words[5])[int(words[6])]
                    bot.high = self.get_collection(words[10])[int(words[11])]

    def execute(self):
        """Execute the factory until there's nothing left to do."""
        q = [(k, v) for k, v in self.inputs.items()]
        while q:
            chip, dest = q.pop(0)
            dest.append(chip)
            if isinstance(dest, Bot) and len(dest) == 2:
                low, high = dest.get_sorted_chips()
                q.append((low, dest.low))
                q.append((high, dest.high))
                dest.clear()

    def execute_with_watch(self, chips: set) -> int | None:
        """Execute the factory and watch for a bot holding `chips`.

        When the run is complete, return the number of the bot that was holding
        the chips, or None if we did not see any bot holding those chips.
        """
        q = [(k, v) for k, v in self.inputs.items()]
        bot_lookup = {id(v): k for k, v in self.bots.items()}
        result = None
        while q:
            chip, dest = q.pop(0)
            dest.append(chip)
            if isinstance(dest, Bot) and len(dest) == 2:
                low, high = dest.get_sorted_chips()
                if {low, high} == chips:
                    result = bot_lookup[id(dest)]

                q.append((low, dest.low))
                q.append((high, dest.high))
                dest.clear()
        return result


def run(stream, test=False, draw=False):
    factory = Factory()
    factory.parse(stream)

    if test:
        factory.execute()
        result1 = dict(factory.outputs)
    else:
        result1 = factory.execute_with_watch({17, 61})

    bins = {0, 1, 2}
    result2 = math.prod(v[0] for k, v in factory.outputs.items() if k in bins)
    return (result1, result2)
