from utils import *


@dataclass
class Number:
    start: int
    end: int
    value: int


@dataclass
class Symbol:
    col: int
    symbol: str


@dataclass
class PartNumber:
    number: Number
    symbol: Symbol


def parse_numbers(line):
    def gen():
        for match in re.finditer("\d+", line):
            yield Number(match.start(), match.end(), int(line[match.start():match.end()]))
    return fit(gen()).tuple()


def parse_symbols(line):
    def gen():
        for match in re.finditer("|".join(f"\\{s}" for s in ('+', '*', '#', '$', '=', '&', '%', '-', '/', '@')), line):
            yield Symbol(match.start(), line[match.start()])
    return fit(gen()).tuple()


def is_adjacent(number, symbol):
    return symbol.col in range(number.start - 1, number.end + 1)


def solve(input):
    input = split(input, "\n")
    numbers = input.map(parse_numbers)
    symbols = input.map(parse_symbols)

    part_numbers = fit([])
    for row, numbers_row in numbers.enumerate():
        for number in numbers_row:
            for symbols_row in symbols[max(0, row - 1):row + 2]:
                for symbol in symbols_row:
                    if is_adjacent(number, symbol):
                        part_numbers.append(PartNumber(number, symbol))

    return part_numbers.map(lambda pn: pn.number.value).reduce(add, 0)


with print_duration():
    print("solution:", solve(read("input.txt")))
