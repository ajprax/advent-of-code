# this version can get the right answer, but is non-deterministic.
# on each execution of the script, all calls to solve will return the same value, but not necessarily the correct value
# the only source of non-determinisism should be the order of `molecules` and thus which particular path is taken.
# this implies that something about the order of the set is changing between runs, but consistent across calls.
# possibly memory alignment?

# This also assumes that the first complete solution is always the best (greedy algorithm).
# The non-determinism suggests that this assumption is not entirely valid

# Keeping the greedy algorithm, the non-determinism could be removed by considering all molecules that are
# equally shortest at each step. Unfortunately, this balloons the number of candidates to an impractical degree

from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace(molecule, src, dst):
    for match in re.finditer(src, molecule):
        yield replace_at(molecule, src, dst, match.start())


def solve(input):
    replacements, medicine = split(input, "\n\n")
    replacements = split(replacements, "\n", " => ")

    start = time.time()

    steps = 0
    # molecules = Set((medicine,))
    molecules = Dict({medicine: 0})
    # seen = Set()
    seen = Dict()
    while True:
        # molecule = molecules.min(len)
        # molecules.remove(molecule)
        # print(molecule)
        mins = molecules.keys().mins(len)
        print(len(mins))
        molecule = mins.shuffled().first()
        steps = molecules.pop(molecule)
        if time.time() - start > .5:
            # for m in path:
            #     print(m)
            return None
        if molecule == "e":
            return steps
            # for m in path:
            #     print(m)
            # print("e")
            # return len(path)
        if molecule not in seen or seen[molecule] > steps:
            seen[molecule] = steps
            for dst, src in replacements:
                for next_molecule in replace(molecule, src, dst):
                    if next_molecule not in molecules or molecules[next_molecule] > steps:
                        molecules[next_molecule] = steps + 1


# with print_duration():
print("solution:", solve(read("input.txt")))
# print("solution:", solve(read("input.txt")))
# print("solution:", solve(read("input.txt")))
