# Based on askalski's insights below
# I was able to make a deterministic solver
# rather than just randomizing the rule order and trying again
# we start with the target molecule and work backwards
# we remove all the Rn..Ar patterns
# then we can math the solution by counting the remaining elements
# https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/

from pathlib import Path
import re
from collections import defaultdict

filename = "input.txt"
data = Path(filename).read_text().splitlines()
# test_filename = Path(__file__).stem+"_test.txt"
# test_data = Path(test_filename).read_text().splitlines()

testing_mode = False

def solve(data):
    replacements,molecule = parse_p2(data)
    return minimum_steps_to_make_cleaned(molecule,replacements)


def parse_p2(data: list[str]):
    molecule = data[-1] # data[-1] means last line
    replacements = [
        (m[1],m[0]) # note we swap from(m[0]) and to(m[1]) here because we're working backwards (staring with target)
        for m
        in re.findall( r"(\w+) => (\w+)",'\n'.join(data[:-2]) )
    ]
    return replacements,molecule


regex_rnar = re.compile(r'([A-Z][a-z]?Rn([^Rr]+)Ar)')
regex_blocker = re.compile(r'([A-Z][a-z]?[A-Z][a-z]?)Rn[^Rr]+Ar')
regex_one_element = re.compile(r'[A-Z][a-z]?')
regex_two_elements = re.compile(r'^[A-Z][a-z]?[A-Z][a-z]?$')
def minimum_steps_to_make_cleaned(molecule,replacements):
    repl_RnAr,repl_doubles,repl_e = split_replacements(replacements)
    answers = []
    mol_0 = molecule
    steps = 0
    clean = False
    while not clean:
        if not regex_rnar.findall(mol_0):
            # no more Rn..Ar, Yey!
            clean = True
            continue

        # reduce all the inner parts of each Rn..Ar pair
        mol_1,steps = replace_inners(mol_0,steps,repl_doubles,repl_RnAr)

        # perform direct xRn..Ar replacements
        mol_2,steps = apply_RnAr(mol_1,steps,repl_RnAr)

        if mol_2 == mol_0:
            # if no changes this cycle
            # but still have Rn..Ar sets
            # then we have one or more special blockers
            mol_2,steps = clear_blockers(mol_0,steps,repl_doubles)
            if mol_2 == mol_0: raise AssertionError("Clearing Blockers failed, we're stuck")
        mol_0 = mol_2

    # now that all Rn..Ar are removed
    # all replacements from now on remove exactly 1 element
    # so we can just count all the remaining elements and math the answer
    answers.append( steps+count_elements(mol_0)-1 ) # -1 because we start with 1 "element": the electron
    return min(answers)

def count_elements(molecule):
    return len(regex_one_element.findall(molecule))

def split_replacements(replacements: list[tuple[str,str]]) -> tuple[list,list,list]:
    repl_RnAr,repl_doubles,repl_e = [],[],[]
    for replacement in replacements:
        if   "Rn" in replacement[0]:
            repl_RnAr.append(replacement)
        elif "e" == replacement[1]:
            repl_e.append(replacement)
        else:
            repl_doubles.append(replacement)
    return repl_RnAr,repl_doubles,repl_e

def clear_blockers(molecule,steps,repl_doubles):
    blockers = []

    # for each Rn..Ar, grab the 2 preceeding elements, store their positions in `blockers`
    for match in regex_blocker.finditer(molecule):
        start,end = match.span(1) # 1 because it's the first capture group
        blockers.append( (start,end) )

    # for each of the found spans
    # perform the only possible replacement
    for start,end in blockers[::-1]: # [::-1] means reversed.  We start replacing from the end to avoid corrupting indexes
        blocker0 = molecule[start:end]
        if blocker0 in [_frm for _frm,_ in repl_doubles]:
            # possible bug here if there's an ambiguous replacement swap
            # (ex. if HP shows up twice in translations like O => HP, H => HP).
            # But I'm pretty sure this is designed not to occur
            to = [_to for _frm,_to in repl_doubles if _frm == blocker0][0]
            molecule = molecule[:start]+to+molecule[end:]
            steps += 1
        else:
            raise AssertionError("edge case encountered: stuck on an Rn..Ar, suspect the element(s) immediately before Rn need to be replaced, but having trouble finding the replacement")
    return molecule,steps

# perform direct xRn..Ar replacements
def apply_RnAr(molecule: str,steps:int,repl_RnAr: list):
    check = re.compile("|".join([f'.*{frm}.*' for frm,_ in repl_RnAr]))
    while check.match(molecule):
        for frm,to in repl_RnAr:
            if frm in molecule:
                molecule = molecule.replace(frm,to,1)
                steps += 1
    return molecule,steps

# reduce all the inner parts of each Rn..Ar pair
# to something that matches one of the direct replacement rules
def replace_inners(starting_molecule: str, steps:int, repl_doubles: list, repl_RnAr: list):
    molecule = starting_molecule
    inners = []

    # grab a Set of the inner elements between Rn and Ar in the replacement options
    # we use this in comparisons later on
    inners_RnAr = {regex_rnar.match(frm).group(2) for frm,_ in repl_RnAr}

    # Find a list of the inner spans between Rn and Ar in the molecule
    for match in regex_rnar.finditer(molecule):
        start,end = match.span(2) # 2 because it's the second capture group
        inners.append( (start,end) )

    # For each inner span we found above
    # Perform elemental replacements on the inner span
    # until it matches one of the target RnAr replacement combinations (inners_RnAr)
    for start,end in inners[::-1]: # [::-1] means reversed.  We start replacing from the end first to avoid corrupting indexes
        inner0 = molecule[start:end]
        steps0 = steps
        min_steps = 1e9
        clean = set()
        q = [(inner0,steps0)] # technically it's a stack, but the differences don't matter for this application
        processed = defaultdict(lambda: 1e9)

        # perform elemental replacements on this span
        # until it matches one of the target RnAr replacement combinations (inners_RnAr)
        while q:
            inner1,steps1 = q.pop()
            if steps1 > min_steps:
                # already worse than best
                continue
            if inner1 in inners_RnAr:
                # matches one of the target combinations
                clean.add( (inner1,steps1) )
                min_steps = min(min_steps,steps1)
                continue
            for frm,to in repl_doubles:
                if frm in inner1:
                    inner2 = inner1.replace(frm,to,1)
                    steps2 = steps1+1
                    if steps2 >= processed[inner2]:
                        # if we've already processed this step more efficiently, don't add this branch to the queue
                        continue
                    q.append( (inner2,steps2) )
                    processed[inner2]=steps2

        # If there's only one final version of the inner span (Ideally this should be true)
        # Select the fastest way to get to it
        # And replace the inner span in the actual molecule
        if len({inner for inner,_ in clean}) == 1:
            steps = min({_steps for _,_steps in clean})
            inner3 = list(clean)[0][0] # easiest way to extract from a set is to convert it to a list (see https://stackoverflow.com/a/48874729/1229736 )
            molecule = molecule[:start] + inner3 + molecule[end:]
        else:
            raise AssertionError("Ambiguous replacements")
        # then repeat for the next inner span
    return molecule,steps


print(solve(data))