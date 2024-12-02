# the replacement rules describe a context-free grammar with "e" as the start symbol
# ambiguity tbd, but probably not


from re import escape


from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


def replace_one(molecule, src, dst):
    m = re.search(escape(src), molecule)
    return m and replace_at(molecule, src, dst, m.start())


def replace_each(molecule, src, dst):
    for match in re.finditer(escape(src), molecule):
        yield replace_at(molecule, src, dst, match.start())


def replace_all(molecule, src, dst):
    for match in reversed(tuple(re.finditer(escape(src), molecule))):
        molecule = replace_at(molecule, src, dst, match.start())
    return molecule


def terminal_and_nonterminal_symbols(replacements):
    def mark_nonterminals(s):
        for nonterminal in nonterminals:
            s = replace_all(s, nonterminal, "º")
        return s

    # non-terminal
    nonterminals = replacements.map(itemgetter(0)).set().list().sorted()
    # terminal
    terminals = replacements.map(itemgetter(1)).map(mark_nonterminals).filter().set()
    terminals = terminals.flat_map(lambda term: term.split("º")).set().filter().list().sorted()
    return terminals, nonterminals


def split_by_terminals(s, terminals):
    for i in range(len(s)):
        for terminal in terminals:
            if i + len(terminal) <= len(s) and s[i:i + len(terminal)] == terminal:
                return List([s[:i], terminal]).filter() + split_by_terminals(s[i + len(terminal):], terminals)
    return List([s]).filter()


def solve(input):
    # input = input.replace("Ar", ")").replace("Rn", "(").replace("Y", ",")
    rules, medicine = split(input, "\n\n")
    rules = split(rules, "\n", " => ")
    # rules.for_each(ic)
    terminals, nonterminals = terminal_and_nonterminal_symbols(rules)
    terminals.for_each(print)
    print()
    nonterminals.for_each(print)
    return
    # ic(terminals, nonterminals)

    # divide the target by terminals
    # medicine = split_by_terminals(medicine, terminals)
    # ic(medicine)
    #
    # show = False
    # @cache
    # def reduce(s):
    #     """return the number of reduction steps and the resulting string"""
    #     for dst, src in rules:
    #         if s == src:
    #             print("atomized", s, dst)
    #             return dst, 1
    #     reduced, steps = (
    #         rules.iter()
    #         .flat_map(t(lambda dst, src: replace_each(s, src, dst)))
    #         .debug(print, show)
    #         .map(lambda s2: reduce(s2))
    #         .min(default=(None, None))
    #     )
    #     if reduced is None:
    #         print("irreducible", s)
    #         return s, 0
    #     print("reduced", s, reduced, steps + 1)
    #     return reduced, steps + 1
    #
    # total_steps = 0
    # # reduce each sections as much as possible
    # for i in range(len(medicine)):
    #     reduced, steps = reduce(medicine[i])
    #     total_steps += steps
    #     medicine[i] = reduced
    # print(total_steps, medicine)
    # print("".join(medicine))

    total_steps = 0
    medicine = "".join(medicine)
    # greedily apply remainig rules
    while medicine != "e":
        for dst, src in rules.sorted(t(lambda d, s: (len(s) - len(d), len(s) + len(d), s, d)), reverse=True):
        # for dst, src in rules.shuffled():
            next_steps = medicine.count(src)
            if next_steps:
                medicine = replace_all(medicine, src, dst)
                total_steps += next_steps
                break
            # if next and next != medicine:
            #     print(src, "=>", dst, "=", next)
            #     medicine = next
            #     total_steps += 1
            #     break
        else:
            print("dead end:", medicine)
            return None
    return total_steps


with print_duration():
    print("solution:", solve(read("input.txt")))