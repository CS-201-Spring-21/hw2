from game import *
from urllib.request import urlopen

casefile = "https://waqarsaleem.github.io/cs201/hw2/cases.txt"


class Case:
    def __init__(self, start: [(int, int)], stop: [(int, int)], steps: int):
        self.start, self.stop, self.steps = start, stop, steps

    def __repr__(self) -> str:
        return f'start: {self.start}\nsteps: {self.steps}\n'\
            f'stop: {self.stop}'


def fetch_testcases(path: str) -> [Case]:
    testcases = []
    if path.startswith('http'):
        input_lines = [line.decode('utf-8').strip()
                       for line in urlopen(path).readlines()]
    else:
        input_lines = open(path).readlines()
    line = iter(input_lines)
    test_count = int(next(line))
    for _ in range(test_count):
        start = list(map(int, next(line).strip().split()))
        start = [tuple(start[i: i+2]) for i in range(0, len(start), 2)]
        steps = int(next(line))
        stop = list(map(int, next(line).strip().split()))
        stop = [tuple(stop[i: i+2]) for i in range(0, len(stop), 2)]
        testcases.append(Case(start, stop, steps))
    return testcases


cases = fetch_testcases(casefile)


def test():
    config = Config()
    config.animate = False
    for case in cases:
        config.rounds = case.steps
        config.start = case.start
        life = Life(config.start)
        Game.run(life, config)
        assert sorted(case.stop) == sorted(life.state()),\
            f'reference: {sorted(case.stop)} does not match '\
            f'generated: {sorted(life.state())}'
