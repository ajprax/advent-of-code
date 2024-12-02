# corrected greedy algorithm. too slow, too much memory despite some optimizations


from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace(molecule, src, dst):
    for match in re.finditer(src, molecule):
        yield replace_at(molecule, src, dst, match.start())


def next_molecules(molecule, replacements):
    def gen():
        for dst, src in replacements:
            for next_molecule in replace(molecule, src, dst):
                yield next_molecule
    return Iterator(gen())


def solve(input):
    replacements, medicine = split(input, "\n\n")
    replacements = split(replacements, "\n", " => ")

    molecules = Dict({
        len(medicine): Dict({
            0: Set([medicine])
        })
    })

    def add(steps):
        def inner(molecule):
            molecules.setdefault(len(molecule), Dict({steps: Set()})).setdefault(steps, Set()).add(molecule)
        return inner

    seen = Set()
    while True:
        min_length = molecules.keys().min()
        min_steps = molecules[min_length].keys().min()
        candidates = molecules[min_length].pop(min_steps)
        if not molecules[min_length]:
            del molecules[min_length]
        if len(candidates.iter().next()) == 1 and candidates.any(lambda molecule: molecule == "e"):
            return min_steps
        (
            candidates
            .filter(seen.add)
            .for_each(lambda candidate: (
                next_molecules(candidate, replacements)
                .for_each(add(min_steps + 1)))
            )
        )


with print_duration():
    print("solution:", solve(read("input.txt")))
