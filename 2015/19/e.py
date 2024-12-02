from math import isfinite

from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace_left(molecule, src, dst):
    return replace_at(molecule, src, dst, molecule.index(src))


def replace_right(molecule, src, dst):
    return replace_at(molecule, src, dst, molecule.rindex(src))


def find_left(s, sub):
    try:
        return s.index(sub)
    except ValueError:
        return None


def find_right(s, sub):
    try:
        return s.rindex(sub)
    except ValueError:
        return None


def solve(input):
    rules, medicine = split(input, "\n\n")
    rules = split(rules, "\n", " => ")

    best = inf
    searched = 0
    search = [(0, medicine)]
    while search:
        steps, molecule = search.pop()
        searched += 1
        if not searched % 100000:
            print(searched, steps, molecule)
        if molecule == "e":
            if steps < best:
                steps = best
                print("found better path with length:", steps)
            else:
                print("found worse path with length:", steps)
        else:
            # for each rule, consider it only if it would have been the leftmost application
            # for src, dst in rules.sorted(t(lambda src, dst: (len(src) - len(dst)))):
            # for src, dst in rules.sorted(itemgetter(1), reverse=True):
            for src, dst in rules:
                try:
                    next = replace_left(molecule, dst, src)
                    if find_left(molecule, dst) == find_left(next, src):
                        search.append((steps + 1, next))

                except ValueError:
                    pass

                # try:
                #     next = replace_right(molecule, dst, src)
                #     if find_right(next, src) == find_right(molecule, dst):
                #         search.append((steps + 1, next))
                # except ValueError:
                #     pass

                # si = find_left(molecule, src)
                # di = find_left(molecule, dst)
                # if di is not None:
                #     if si is None or si >= di:
                #         search.append((steps + 1, replace_left(molecule, dst, src)))
                #         print("checking", si, src, "=>", dst, di)
                #     else:
                    #     print("skipping", si, src, "=>", dst, di)
                # else:
                #     print("no match", si, src, "=>", dst, di)

                # si = find_right(molecule, src)
                # di = find_right(molecule, dst)
                # if di is not None:
                #     if si is None or si <= di:
                #         search.append((steps + 1, replace_right(molecule, dst, src)))
                #         print("checking", si, src, "=>", dst, di)
                #     else:
                #         print("skipping", si, src, "=>", dst, di)
                # else:
                #     print("no match", si, src, "=>", dst, di)
            # print("-"*20)
    return best


with print_duration():
    print("solution:", solve(read("input.txt")))
