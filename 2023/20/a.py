from dataclasses import field
from utils import *


@dataclass
class Broadcaster:
    dest: List[str]
    name: str = "broadcaster"

    def recv(self, name: str, pulse: bool):
        return self.dest.map(lambda name: (self.name, name, pulse))


@dataclass
class FlipFlop:
    name: str
    dest: List[str]
    on: bool = False

    def recv(self, name: str, pulse: bool):
        # ignore high pulses
        if pulse:
            return ()
        self.on = out = not self.on
        return self.dest.map(lambda name: (self.name, name, out))


@dataclass
class Conjunction:
    name: str
    dest: List[str]
    inputs: Dict[str, bool] = field(default_factory=Dict)

    def recv(self, name: str, pulse: bool):
        self.inputs[name] = pulse
        out = not self.inputs.values().all()
        return self.dest.map(lambda name: (self.name, name, out))


class Output:
    def recv(self, name: str, pulse: bool):
        return ()


def parse(input):
    def parse_line(line):
        l, r = line.split(" -> ")
        destinations = List(r.split(", "))
        if l == "broadcaster":
            return "broadcaster", Broadcaster(destinations)
        if l[0] == "%":
            name = l[1:]
            return name, FlipFlop(name, destinations)
        if l[0] == "&":
            name = l[1:]
            return name, Conjunction(name, destinations)
    modules = List(input.split("\n")).map(parse_line).dict()
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            for input_name, input_module in modules.items():
                if name in input_module.dest:
                    module.inputs[input_name] = False
    modules["output"] = Output()
    modules["rx"] = Output()
    return modules


def press(modules):
    high = low = 0
    to_send = List([("button", "broadcaster", False)])
    while to_send:
        h, l = to_send.partition(itemgetter(2))
        high += h.size()
        low += l.size()
        to_send = to_send.flat_map(t(lambda from_, to, pulse: modules[to].recv(from_, pulse)))
    return high, low


def solve(input):
    initial_modules = parse(input)
    modules = deepcopy(initial_modules)
    high = low = 0
    for i in range(1, 1001):
        h, l = press(modules)
        high += h
        low += l
        if modules == initial_modules:
            break
    return int(high * low * 1000000 / i**2)


sample_actual = solve(read("sample1.txt"))
sample_expected = 32000000
assert sample_expected == sample_actual, (sample_expected, sample_actual)

sample_actual = solve(read("sample2.txt"))
sample_expected = 11687500
assert sample_expected == sample_actual, (sample_expected, sample_actual)


with print_duration():
    print("solution:", solve(read("input.txt")))