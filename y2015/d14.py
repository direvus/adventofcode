import re
from collections import defaultdict


PATTERN = re.compile(r'(\w+) .+ (\d+) .+ (\d+) .+ (\d+)')


class Reindeer:
    def __init__(self, name: str, speed: int, runtime: int, resttime: int):
        self.name = name
        self.speed = speed
        self.runtime = runtime
        self.resttime = resttime
        self.running = True
        self.timer = 0
        self.position = 0

    def tick(self) -> int:
        """Adjust this reindeer for the next tick of time.

        Return the reindeer's new position at the end of the tick.
        """
        if self.running and self.timer >= self.runtime:
            # Time for a rest
            self.running = False
            self.timer = 0
        elif not self.running and self.timer >= self.resttime:
            # Time to get running again
            self.running = True
            self.timer = 0

        if self.running:
            self.position += self.speed
        self.timer += 1
        return self.position


class Race:
    def __init__(self):
        self.runners = []
        self.scores = defaultdict(lambda: 0)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PATTERN.match(line)
            if not m:
                print(f"'{line}' didn't match")
                continue
            name, speed, runtime, resttime = m.groups()
            speed = int(speed)
            runtime = int(runtime)
            resttime = int(resttime)

            self.runners.append(Reindeer(name, speed, runtime, resttime))

    def run(self, time: int):
        for t in range(time):
            best = float('-inf')
            leaders = set()
            for i, r in enumerate(self.runners):
                pos = r.tick()
                if pos > best:
                    leaders = {i}
                    best = pos
                elif pos == best:
                    leaders.add(i)
            for i in leaders:
                self.scores[i] += 1

    def get_winning_distance(self) -> int:
        return max([x.position for x in self.runners])

    def get_winning_score(self) -> int:
        return max(self.scores.values())


def run(stream, test=False):
    race = Race()
    race.parse(stream)
    t = 1000 if test else 2503
    race.run(t)
    result1 = race.get_winning_distance()
    result2 = race.get_winning_score()
    return (result1, result2)
