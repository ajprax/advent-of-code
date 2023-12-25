from utils import *


@dataclass
class Number:
    row: int
    start: int
    end: int
    value: int


@dataclass(unsafe_hash=True)
class Symbol:
    row: int
    col: int
    symbol: str


@dataclass
class PartNumber:
    number: Number
    symbol: Symbol


def parse_numbers(row, line):
    def gen():
        for match in re.finditer("\d+", line):
            yield Number(row, match.start(), match.end(), int(line[match.start():match.end()]))
    return fit(gen()).tuple()


def parse_symbols(row, line):
    def gen():
        for match in re.finditer("|".join(f"\\{s}" for s in ('+', '*', '#', '$', '=', '&', '%', '-', '/', '@')), line):
            yield Symbol(row, match.start(), line[match.start()])
    return fit(gen()).tuple()


def is_adjacent(number, symbol):
    return symbol.col in range(number.start - 1, number.end + 1)


def solve(input):
    input = split(input, "\n")
    numbers = input.enumerate().map(t(parse_numbers))
    symbols = input.enumerate().map(t(parse_symbols))

    part_numbers = fit([])
    for row, numbers_row in numbers.enumerate():
        for number in numbers_row:
            for symbols_row in symbols[max(0, row - 1):row + 2]:
                for symbol in symbols_row:
                    if is_adjacent(number, symbol):
                        part_numbers.append(PartNumber(number, symbol))

    return (
        part_numbers
        .filter(lambda pn: pn.symbol.symbol == "*")
        .group_by(lambda pn: pn.symbol)
        .filter_values(lambda numbers: len(numbers) == 2)
        .values()
        .map(t(lambda a, b: a.number.value * b.number.value))
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
