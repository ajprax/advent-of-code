from utils import *


def build_graphs(lines):
    forward = defaultdict(list)
    backward = defaultdict(list)
    for line in lines:
        match line.split():
            case [a, "AND", b, "->", o]:
                forward[a].append(("AND", b, o))
                forward[b].append(("AND", a, o))
                backward[o].extend((a, b))
            case [a, "OR", b, "->", o]:
                forward[a].append(("OR", b, o))
                forward[b].append(("OR", a, o))
                backward[o].extend((a, b))
            case [a, "RSHIFT", bits, "->", o]:
                bits = int(bits)
                forward[a].append(("RSHIFT", bits, o))
                backward[o].append(a)
            case [a, "LSHIFT", bits, "->", o]:
                bits = int(bits)
                forward[a].append(("LSHIFT", bits, o))
                backward[o].append(a)
            case ["NOT", a, "->", o]:
                forward[a].append(("NOT", o))
                backward[o].append(a)
            case [a, "->", o]:
                forward[a].append((o,))
                backward[o].append(a)
    return Dict(forward), Dict(backward)


def get_wire_names(line):
    match line.split():
        case [a, "AND", b, "->", o]:
            return a, b, o
        case [a, "OR", b, "->", o]:
            return a, b, o
        case [a, "RSHIFT", _, "->", o]:
            return a, o
        case [a, "LSHIFT", _, "->", o]:
            return a, o
        case ["NOT", a, "->", o]:
            return a, o
        case [a, "->", o]:
            return a, o


@dataclass(unsafe_hash=True)
class Wire:
    name: str
    value: int = 0
    has_value: bool = False

    def __post_init__(self):
        try:
            self.value = int(self.name)
            self.has_value = True
        except ValueError:
            pass

    def set(self, value):
        self.value = value
        self.has_value = True


def solve(input):
    wires = split(input, "\n").flat_map(get_wire_names).set().map_to_values(Wire)
    forward, backward = build_graphs(split(input, "\n"))

    # update for part 2
    wires["b"].set(46065)
    for name in backward["b"]:
        wires.pop(name)

    seen = Set()
    signals = wires.values().filter(lambda wire: wire.has_value).list()
    while signals:
        signal = signals.pop()
        for output in forward.get(signal.name, ()):
            match output:
                case ["AND", b, o]:
                    if wires[b].has_value and seen.add((signal, "AND", wires[b], wires[o])):
                        wires[o].set((signal.value & wires[b].value) % 65536)
                        signals.append(wires[o])
                case ["OR", b, o]:
                    if wires[b].has_value and seen.add((signal, "OR", wires[b], wires[o])):
                        wires[o].set((signal.value | wires[b].value) % 65536)
                        signals.append(wires[o])
                case ["RSHIFT", bits, o]:
                    if seen.add((signal, "RSHIFT", bits, wires[o])):
                        wires[o].set((signal.value >> bits) % 65536)
                        signals.append(wires[o])
                case ["LSHIFT", bits, o]:
                    if seen.add((signal, "LSHIFT", bits, wires[o])):
                        wires[o].set((signal.value << bits) % 65536)
                        signals.append(wires[o])
                case ["NOT", o]:
                    if seen.add(("NOT", signal, wires[o])):
                        wires[o].set((~signal.value) % 65536)
                        signals.append(wires[o])
                case [o]:
                    if seen.add((signal, wires[o])):
                        wires[o].set(signal.value)
                        signals.append(wires[o])

    return wires["a"].value


with print_duration():
    print("solution:", solve(read("input.txt")))
