import itertools

from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace_all(molecule, src, dst):
    for match in reversed(tuple(re.finditer(re.escape(src), molecule))):
        molecule = replace_at(molecule, src, dst, match.start())
    return molecule


def terminal_and_nonterminal_symbols(replacements):
    def mark_nonterminals(s):
        for nonterminal in nonterminals:
            s = replace_all(s, nonterminal, "º")
        return s

    nonterminals = replacements.map(itemgetter(0)).set().list().sorted()
    terminals = replacements.map(itemgetter(1)).map(mark_nonterminals).filter().set()
    terminals = terminals.flat_map(lambda term: term.split("º")).set().filter().list().sorted()
    return terminals, nonterminals


def split_by_terminals(s, terminals):
    for i in range(len(s)):
        for terminal in terminals:
            if i + len(terminal) <= len(s) and s[i:i + len(terminal)] == terminal:
                return List([s[:i], terminal]).filter() + split_by_terminals(s[i + len(terminal):], terminals)
    return List([s]).filter()


def pprint(molecule, terminals):
    molecule = split_by_terminals(molecule, terminals)
    indent = 0
    for s in molecule:
        sindent = indent
        if "(" in s:
            indent += 2
        elif ")" in s:
            sindent -= 2
            indent -= 2
        print(f"{sindent * ' '}{s}")


def find_paired_parens(s):
    def gen():
        opens = []
        for i in range(len(s)):
            if s[i] == "(":
                opens.append(i)
            elif s[i] == ")":
                yield opens.pop(), i, len(opens)
        assert not opens
    return Tuple(gen()).sorted()


from colorama import Back
def red(c):
    return Back.RED + c + Back.RESET
def green(c):
    return Back.GREEN + c + Back.RESET


def show_paren_pairs(s, pairs):
    chars = List()
    for (o, c, depth) in pairs:
        if depth % 2:
            chars.append(("red", "(", o))
            chars.append(("red", ")", c))
        else:
            chars.append(("green", "(", o))
            chars.append(("green", ")", c))
    for color, symbol, index in chars.sorted(itemgetter(2), reverse=True):
        s = replace_at(s, symbol, globals()[color](symbol), index)
    print(s)


def show_paren_maxima(s, parens):
    chars = List()
    for i, d in parens:
        if d % 2:
            chars.append(("red", s[i], i))
        else:
            chars.append(("green", s[i], i))
    for color, symbol, index in chars.sorted(itemgetter(2), reverse=True):
        s = replace_at(s, symbol, globals()[color](symbol), index)
    print(s)


def find_maximum_parens(s):
    return (
        Tuple(re.finditer("[\(\)]", s)).map(lambda m: m.start())
        .sliding(2)
        .filter(t(lambda o, c: s[o] == "(" and s[c] == ")"))
    )


def suffixes(s):
    def gen():
        for i in range(len(s)):
            yield s[i:]
    return Iterator(gen())


def conflicts(a, b):
    return suffixes(a).any(b.startswith) or suffixes(b).any(a.startswith)


def apply_rules(s, rules):
    steps = 0
    for src, dst in rules:
        steps += s.count(dst)
        s = replace_all(s, dst, src)
    return s, steps


def group_by_interference(rules):
    # rules are vertices and edges indicate conflicts
    graph = rules.map_to_values(lambda rule: Set())
    for a, b in rules.combinations(2):
        if conflicts(a[1], b[1]):
            graph[a].add(b)
            graph[b].add(a)
    graph = Dict(graph)
    # a group is all mutually reachable vertices
    groups = List()
    for rule in graph.keys():
        if groups.any(lambda group: rule in group):
            continue

        reachable = Set()
        search = [rule]
        while search:
            other = search.pop()
            if reachable.add(other):
                search.extend(graph[other])
        groups.append(reachable)
    return groups




def solve(input):
    input = input.replace("Ar", ")").replace("Rn", "(").replace("Y", ",")
    rules, medicine = split(input, "\n\n")
    rules = split(rules, "\n", " => ").map(Tuple)
    terminals, nonterminals = terminal_and_nonterminal_symbols(rules)

    # simplify the contents of all parens at the maximum depth - this won't remove any parens
    # simplify all parens at the next greatest depth - this should remove the maximum depth parens
    # re-find parens and simplify at the second greatest depth
    # repeat until there is only 1 depth
    # simplify all that remains

    highest = 0
    @cache
    def simplify(s):
        nonlocal highest
        # to start, just naively apply rules until none apply
        steps = 0
        while True:
            # determine which rules apply, return the shortest simplification based on all possible orderings of those rules
            applicable_rules = rules.filter(t(lambda src, dst: dst in s))
            # the full permutations are too numerous. instead find rules that might conflict and only consider orderings of those
            # e.g. ThCa => Ca and SiTh => Ca conflict because the end of one overlaps the beginning of the other
            # SiThCa can simplify to SiCa via ThCa => Ca or to CaCa via SiTh => Ca
            # TODO: a possible further optimization is to look at the lhs of conflicting rules and see if the new value
            #  is equal to the overlap
            if len(applicable_rules) > 1:
                groups = group_by_interference(applicable_rules)
                # within a group ordering matters, but across groups it doesn't, so take the permutations of rules within each group and product them
                orderings = Iterator(itertools.product(*groups.map(lambda group: group.permutations()))).map(lambda ordering: Tuple(ordering).flatten())
                # try all orderings and return the best result
                # TODO: a complication: we may not know the best ordering until we have run the process repeatedly

                # nodes = List()
                # for ai in range(len(applicable_rules)):
                #     has_conflict = False
                #     for bi in range(ai + 1, len(applicable_rules)):
                #         a = applicable_rules[ai]
                #         b = applicable_rules[bi]
                #         if conflicts(a[1], b[1]):
                #             has_conflict = True
                #             nodes.append([a, b])
                #     if not has_conflict:
                #         nodes.append([a])
                # if "b" in locals():
                #     nodes.append([b])
                # print("nodes:")
                # for node in nodes:
                #     print(node)
                #
                # print("flattened")
                # Iterator(itertools.product(*nodes.map(lambda node: Tuple(node).permutations()).flatten())).map(lambda order: Tuple(order).distinct()).distinct().for_each(print)





                # print(s)
                # print("applicable", len(applicable_rules))
                # applicable_rules.for_each(print)
                # orderable = List()
                # for a, b in applicable_rules.combinations(2):
                #     if conflicts(a[1], b[1]):
                #         orderable.append([(a, b), (b, a)])
                #     # else:
                #     #     print(a, b, "no conflict")
                #     #     orderable.append([(a,), (b,)])
                # print(applicable_rules.set())
                # print(orderable.flatten().flatten())
                # print(orderable.flatten().flatten().set())
                # orderable.extend((applicable_rules.set() - orderable.flatten().flatten().set()).map(lambda rule: Tuple((rule,))))
                # print("orderable", orderable.size())
                # orderable.for_each(print)
                # ordered = Iterator(itertools.product(*orderable)).map(lambda order: Tuple(order).flatten().distinct()).distinct().tuple()
                # print("ordered", ordered.size())
                # ordered.for_each(print)


            # find conflicting pairs and add them to a list along with all individual rules as singleton tuples
            # product the tuples and then distinct them to get all meaningful orderings
            s_, steps_ = apply_rules(s, rules)
            if s == s_:
                return s, steps
            else:
                s = s_
                steps += steps_

    # print(simplify("SiThCaRnFAr", rules))
    # print(simplify("PBCaCaSi(F,SiThCa(F))CaCaSi", rules))
    # return

    total_steps = 0
    while True:
        paren_pairs = find_paired_parens(medicine)
        max_depth = paren_pairs.map(itemgetter(2)).max()
        for depth in range(max_depth, -1, -1):
            simplified_any = False
            for o, c, d in paren_pairs.filter(t(lambda o, c, d: d == depth)).sorted(reverse=True):
                simplified, steps = simplify(medicine[o+1:c])
                if steps:
                    simplified_any = True
                    total_steps += steps
                    # print(depth, o, c, d, medicine[o+1:c], steps, simplified)
                    medicine = replace_at(medicine, medicine[o+1:c], simplified, o+1)
            if simplified_any:
                break
        else:
            # interiors cannot be simplified any more, so simplify all that remains
            medicine, steps = simplify(medicine)
            # print(steps, medicine)
            if steps:
                total_steps += steps
                if medicine == "e":
                    return total_steps
            else:
                assert False, f"dead end {medicine}"
        # print("total steps:", total_steps, medicine)

    # total_steps = 0
    # for _ in range(3):
    #     paren_pairs = find_paired_parens(medicine)
    #     max_depth = paren_pairs.map(itemgetter(2)).max()
    #     max_depth_pairs = paren_pairs.filter(t(lambda o, c, d: d == max_depth)).sorted(reverse=True)
    #     # print(max_depth)
    #     # print(max_depth_pairs)
    #     for o, c, d in max_depth_pairs:
    #         simplified, steps = simplify(medicine[o+1:c], rules)
    #         if steps:
    #             total_steps += steps
    #             print(o, c, d, medicine[o+1:c], steps, simplified)
    #             medicine = replace_at(medicine, medicine[o+1:c], simplified, o+1)
    #     second_depth_pairs = paren_pairs.filter(t(lambda o, c, d: d + 1 == max_depth)).sorted(reverse=True)
    #     for o, c, d in second_depth_pairs:
    #         simplified, steps = simplify(medicine[o+1:c], rules)
    #         if steps:
    #             total_steps += steps
    #             print(o, c, d, medicine[o+1:c], steps, simplified)
    #             medicine = replace_at(medicine, medicine[o+1:c], simplified, o+1)
    #     # print(medicine)
    #     print("total steps:", total_steps)
    # for o, c in find_maximum_parens(medicine).reversed():
    #     print(o, c, medicine[o+1:c])

    # for each pair of open and close parens, simplify the inside
    # paren_pairs = find_paired_parens(medicine)
    # parens = paren_pairs.flat_map(t(lambda o, c, d: [(o, d), (c, d)])).sorted()
    # show_paren_pairs(medicine, paren_pairs)
    # # find depth maxima and show only those
    # maxima = List()
    # for pi in range(len(parens)):
    #     i, d = parens[pi]
    #     if medicine[i] == "(":
    #         if medicine[parens[pi+1][0]] == ")":
    #             maxima.append(parens[pi])
    #     elif medicine[i] == ")":
    #         if medicine[parens[pi-1][0]] == "(":
    #             maxima.append(parens[pi])
    #     else:
    #         assert False
    # show_paren_maxima(medicine, maxima)
    #     # show_paren_pairs(medicine, [paren_pairs[i]])



    # steps = 0
    # print(steps, len(medicine))
    # for src, dst in rules:
    #     if "(" in dst:
    #         steps += medicine.count(dst)
    #         medicine = replace_all(medicine, dst, src)
    # print(steps, len(medicine))
    # pprint(medicine, terminals)

with print_duration():
    print("solution:", solve(read("input.txt")))