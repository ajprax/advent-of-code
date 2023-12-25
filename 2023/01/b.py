from utils import *


word_to_digit = dict(one="1", two="2", three="3", four="4", five="5", six="6", seven="7", eight="8", nine="9")


def replace(s, i, c):
    return s[:i] + c + s[i + 1:]


def words_to_digits(line):
    replacements = []
    for word in word_to_digit:
        for match in re.finditer(word, line):
            replacements.append((word, match.start()))

    for word, index in replacements:
        line = replace(line, index, word_to_digit[word])

    return line


def solve(input):
    return (
        split(input, "\n")
        .map(words_to_digits)
        .map(lambda line: List(line).filter(lambda char: char in "0123456789"))
        .map(lambda digits: int(digits[0] + digits[-1]))
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
