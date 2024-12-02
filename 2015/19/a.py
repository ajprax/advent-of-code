from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace(molecule, src, dst):
    for match in re.finditer(src, molecule):
        yield replace_at(molecule, src, dst, match.start())


def solve(input):
    replacements, molecule = split(input, "\n\n")
    replacements = split(replacements, "\n", " => ")
    return replacements.flat_map(t(lambda src, dst: replace(molecule, src, dst))).set().size()


with print_duration():
    print("solution:", solve(read("input.txt")))
