from utils import *


def replace_at(molecule, src, dst, index):
    return molecule[:index] + dst + molecule[index + len(src):]


@dataclass(unsafe_hash=True)
class Rule:
    src: str
    dst: str

    def __str__(self):
        return f"{self.src} => {self.dst}"

    def applicable(self, molecule):
        return self.dst in molecule.s

    def apply(self, molecule, index):
        return molecule.apply(self, index)


@dataclass(unsafe_hash=True)
class Molecule:
    s: str

    def __getitem__(self, item):
        return Molecule(self.s[item])

    def apply(self, rule, index):
        return Molecule(replace_at(self.s, rule.src, rule.dst, index))

    def emplace_simplification(self, parens, simplified):
        return Molecule(self.s[:parens.start] + simplified.s + self.s[parens.stop:])

    def paired_parens(self):
        def gen():
            opens = []
            for i in range(len(self.s)):
                if self.s[i] == "(":
                    opens.append(i)
                elif self.s[i] == ")":
                    yield slice(opens.pop() + 1, i), len(opens)
            assert not opens
        return Tuple(gen()).sorted()

    def pprint_parens(self, parens):
        p, d = parens
        print(self.s)
        print(f"{' '*p.start}{self.s[p]}")

simplifications = Dict()


def simplify(molecule, rules):
    if molecule in simplifications:
        return simplifications[molecule]
    working = copy(molecule)
    total_steps = 0
    while True:
        paren_pairs = working.paired_parens()
        if paren_pairs:
            max_depth = paren_pairs.map(itemgetter(1)).max()
            for depth in range(max_depth, -1, -1):
                parens_at_depth = paren_pairs.filter(t(lambda p, d: d == depth)).map(itemgetter(0))
                simplified_any = False
                for p in parens_at_depth.sorted(lambda p: p.stop, reverse=True):
                    simplified, steps = simplify(working[p], rules)
                    working = working.emplace_simplification(p, simplified)
                    if steps:
                        simplified_any = True
                        total_steps += steps
                if simplified_any:
                    break
            else:
                break
        else:
            applicable = rules.filter(lambda rule: rule.applicable(molecule))
            if applicable:

                print(molecule, applicable)
                exit()
            else:
                break
    simplifications[molecule] = working, total_steps
    return working, total_steps


@dataclass
class Derivation:
    steps: List[Tuple[Rule, int]]

    def apply(self, molecule):
        return self.steps.fold(molecule, t(lambda acc, r: acc.apply(*r)))


def solve(input):
    input = input.replace("Ar", ")").replace("Rn", "(").replace("Y", ",")
    rules, medicine = split(input, "\n\n")
    medicine = Molecule(medicine)
    rules = split(rules, "\n", " => ").map(t(Rule))
    m, steps = simplify(medicine, rules)
    assert m.s == "e"
    return steps

with print_duration():
    print("solution:", solve(read("input.txt")))
