from utils import *
from dataclasses import field


@dataclass
class Broadcaster:
    dest: List[str]
    name: str = "broadcaster"

    # returns (name, pulse) pairs for all outgoing pulses
    def recv(self, name: str, pulse: bool):
        return self.dest.map(lambda name: (self.name, name, pulse))


@dataclass
class FlipFlop:
    name: str
    dest: List[str]
    on: bool = False

    # returns (from, to, pulse) triples for all outgoing pulses
    def recv(self, name: str, pulse: bool):
        # ignore high pulses
        if pulse:
            return ()
        self.on = not self.on
        return self.dest.map(lambda name: (self.name, name, self.on))


@dataclass
class Conjunction:
    name: str
    dest: List[str]
    inputs: Dict[str, bool] = field(default_factory=Dict)

    # returns (name, pulse) pairs for all outgoing pulses
    def recv(self, name: str, pulse: bool):
        self.inputs[name] = pulse
        out = not self.inputs.values().all()
        return self.dest.map(lambda name: (self.name, name, out))


class Output:
    def recv(self, name, pulse):
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
    modules = fit(input.split("\n")).map(parse_line).dict()
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            for input_name, input_module in modules.items():
                if name in input_module.dest:
                    module.inputs[input_name] = False
    modules["rx"] = Output()
    return modules


def press(modules, i):
    to_send = List([("button", "broadcaster", False)])
    while to_send:
        next_to_send = List()
        for from_, to, pulse in to_send:
            if from_ != "broadcaster" and to in ("vl", "cs", "cn", "ml") and not pulse:
                print(i, from_, to, pulse)
            for name in ("xl", "ln", "xp", "gp"):
                if from_ == name and pulse:
                    print(f"{name} high at {i}")
            if to == "rx" and not pulse:
                return True
            next_to_send.extend(modules[to].recv(from_, pulse))
        to_send = next_to_send
    return False


def solve(input):
    modules = parse(input)
    for i in count(1):
        if press(modules, i):
            return i


# TODO: try to write a solution that understands the graph automatically and figure out the node periods to LCM, or even
#  better, work the whole graph backwards to understand the relationship between the input and output


# rx depends on df which is a conjunction of xl, ln, xp, gp
# each of these is high after a predictable number of presses
# df will see all high (and rx therefor will see low) after lcm(xl, ln, xp, gp) presses
print(lcm(3833, 4021, 4051, 4057))


# rx will see low when df sees all high at once
# df sources from xl, ln, xp, gp
    # xl sends high when zp sends low
    # ln sends high when pp sends low
    # xp sends high when sj sends low
    # gp sends high when rg sends low


modules = parse(read("input.txt"))
for i in range(1, 10000):
    press(modules, i)