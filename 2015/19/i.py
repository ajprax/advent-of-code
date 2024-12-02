from utils import *


def count_steps(molecule, rules):
    def replace_at(molecule, src, dst, index):
        return molecule[:index] + dst + molecule[index + len(src):]

    def step(molecule, rules):
        for i in range(len(molecule)):
            for src, dst in rules:
                for j in range(len(src)):
                    if i + j >= len(molecule) or src[j] != molecule[i + j]:
                        break
                else:
                    return replace_at(molecule, src, dst, i)

    for steps in count():
        if molecule is None:
            return None
        if molecule == "e":
            return steps
        molecule = step(molecule, rules)


def count_steps_re(molecule, rules):
    rules = rules.dict()
    pattern = re.compile("|".join(rules.keys()))

    def replace(match):
        return rules[match.group()]

    steps = 0
    while molecule != "e":
        molecule, substeps = pattern.subn(replace, molecule)
        steps += substeps
    return steps


def parse(input):
    lines = split(input, "\n").map(lambda line: line[::-1])
    rules = lines[:-2].map(lambda line: line.split(" >= "))
    medicine = lines[-1]
    return medicine, rules


def solve(input):
    medicine, rules = parse(input)
    return count_steps_re(medicine, rules)


with print_duration():
    print("solution:", solve(read("input.txt")))


# TODO: try using non-reversed patterns, but use rfind instead of sub/subn