from lrparsing import Grammar, Token, Ref, List, Repeat, Prio


class Parser(Grammar):
    Al = Token("Al")
    Ar = Token("Ar")
    B = Token("B")
    C = Token("C")
    Ca = Token("Ca")
    F = Token("F")
    H = Token("H")
    Mg = Token("Mg")
    N = Token("N")
    O = Token("O")
    P = Token("P")
    Rn = Token("Rn")
    Si = Token("Si")
    Th = Token("Th")
    Ti = Token("Ti")
    Y = Token("Y")
    e = Token("e")

    # productions
    ThF = Th + F
    ThRnFAr = Th + Rn + F + Ar
    BCa = B + Ca
    TiB = Ti + B
    TiRnFAr = Ti + Rn + F + Ar
    CaCa = Ca + Ca
    PB = P + B
    PRnFAr = P + Rn + F + Ar
    SiRnFYFAr = Si + Rn + F + Y + F + Ar
    SiRnMgAr = Si + Rn + Mg + Ar
    SiTh = Si + Th
    CaF = Ca + F
    PMg = P + Mg
    SiAl = Si + Al
    CRnAlAr = C + Rn + Al + Ar
    CRnFYFYFAr = C + Rn + F + Y + F + Y + F + Ar
    CRnFYMgAr = C + Rn + F + Y + Mg + Ar
    CRnMgYFAr = C + Rn + Mg + Y + F + Ar
    HCa = H + Ca
    NRnFYFAr = N + Rn + F + Y + F + Ar
    NRnMgAr = N + Rn + Mg + Ar
    NTh = N + Th
    OB = O + B
    ORnFAr = O + Rn + F + Ar
    BF = B + F
    TiMg = Ti + Mg
    CRnFAr = C + Rn + F + Ar
    HSi = H + Si
    CRnFYFAr = C + Rn + F + Y + F + Ar
    CRnMgAr = C + Rn + Mg + Ar
    HP = H + P
    NRnFAr = N + Rn + F + Ar
    OTi = O + Ti
    CaP = Ca + P
    PTi = P + Ti
    SiRnFAr = Si + Rn + F + Ar
    CaSi = Ca + Si
    ThCa = Th + Ca
    BP = B + P
    TiTi = Ti + Ti
    HF = H + F
    NAl = N + Al
    OMg = O + Mg

    Atom = Al | Ar | B | C | Ca | F | H | Mg | N | O | P | Rn | Si | Th | Ti | Y | e
    Production = ThF | ThRnFAr | BCa | TiB | TiRnFAr | CaCa | PB | PRnFAr | SiRnFYFAr | SiRnMgAr | SiTh | CaF | PMg | SiAl | CRnAlAr | CRnFYFYFAr | CRnFYMgAr | CRnMgYFAr | HCa | NRnFYFAr | NRnMgAr | NTh | OB | ORnFAr | BF | TiMg | CRnFAr | HSi | CRnFYFAr | CRnMgAr | HP | NRnFAr | OTi | CaP | PTi | SiRnFAr | CaSi | ThCa | BP | TiTi | HF | NAl | OMg
    Phrase = Repeat(Atom)

    START = Phrase


class Parser(Grammar):
    Al = Token("Al")
    B = Token("B")
    C = Token("C")
    Ca = Token("Ca")
    F = Token("F")
    H = Token("H")
    Mg = Token("Mg")
    N = Token("N")
    O = Token("O")
    P = Token("P")
    Si = Token("Si")
    Th = Token("Th")
    Ti = Token("Ti")
    e = Token("e")

    # productions
    ThF = Th + F
    ThRnFAr = Th + "Rn" + F + "Ar"
    BCa = B + Ca
    TiB = Ti + B
    TiRnFAr = Ti + "Rn" + F + "Ar"
    CaCa = Ca + Ca
    PB = P + B
    PRnFAr = P + "Rn" + F + "Ar"
    SiRnFYFAr = Si + "Rn" + F + "Y" + F + "Ar"
    SiRnMgAr = Si + "Rn" + Mg + "Ar"
    SiTh = Si + Th
    CaF = Ca + F
    PMg = P + Mg
    SiAl = Si + Al
    CRnAlAr = C + "Rn" + Al + "Ar"
    CRnFYFYFAr = C + "Rn" + F + "Y" + F + "Y" + F + "Ar"
    CRnFYMgAr = C + "Rn" + F + "Y" + Mg + "Ar"
    CRnMgYFAr = C + "Rn" + Mg + "Y" + F + "Ar"
    HCa = H + Ca
    NRnFYFAr = N + "Rn" + F + "Y" + F + "Ar"
    NRnMgAr = N + "Rn" + Mg + "Ar"
    NTh = N + Th
    OB = O + B
    ORnFAr = O + "Rn" + F + "Ar"
    BF = B + F
    TiMg = Ti + Mg
    CRnFAr = C + "Rn" + F + "Ar"
    HSi = H + Si
    CRnFYFAr = C + "Rn" + F + "Y" + F + "Ar"
    CRnMgAr = C + "Rn" + Mg + "Ar"
    HP = H + P
    NRnFAr = N + "Rn" + F + "Ar"
    OTi = O + Ti
    CaP = Ca + P
    PTi = P + Ti
    SiRnFAr = Si + "Rn" + F + "Ar"
    CaSi = Ca + Si
    ThCa = Th + Ca
    BP = B + P
    TiTi = Ti + Ti
    HF = H + F
    NAl = N + Al
    OMg = O + Mg

    Atom = Al | B | C | Ca | F | H | Mg | N | O | P | Si | Th | Ti | e
    Production = ThF | ThRnFAr | BCa | TiB | TiRnFAr | CaCa | PB | PRnFAr | SiRnFYFAr | SiRnMgAr | SiTh | CaF | PMg | SiAl | CRnAlAr | CRnFYFYFAr | CRnFYMgAr | CRnMgYFAr | HCa | NRnFYFAr | NRnMgAr | NTh | OB | ORnFAr | BF | TiMg | CRnFAr | HSi | CRnFYFAr | CRnMgAr | HP | NRnFAr | OTi | CaP | PTi | SiRnFAr | CaSi | ThCa | BP | TiTi | HF | NAl | OMg
    Phrase = Repeat(Prio(Atom, Production))

    START = Phrase


class ReverseParser(Grammar):
    Al = Token("lA")
    Ar = Token("rA")
    B = Token("B")
    C = Token("C")
    Ca = Token("aC")
    F = Token("F")
    H = Token("H")
    Mg = Token("gM")
    N = Token("N")
    O = Token("O")
    P = Token("P")
    Rn = Token("nR")
    Si = Token("iS")
    Th = Token("hT")
    Ti = Token("iT")
    Y = Token("Y")
    e = Token("e")

    # productions
    ThF = F + Th
    ThRnFAr = Ar + F + Rn + Th
    BCa = Ca + B
    TiB = B + Ti
    TiRnFAr = Ar + F + Rn + Ti
    CaCa = Ca + Ca
    PB = B + P
    PRnFAr = Ar + F + Rn + P
    SiRnFYFAr = Ar + F + Y + F + Rn + Si
    SiRnMgAr = Ar + Mg + Rn + Si
    SiTh = Th + Si
    CaF = F + Ca
    PMg = Mg + P
    SiAl = Al + Si
    CRnAlAr = Ar + Al + Rn + C
    CRnFYFYFAr = Ar + F + Y + F + Y + F + Rn + C
    CRnFYMgAr = Ar + Mg + Y + F + Rn + C
    CRnMgYFAr = Ar + F + Y + Mg + Rn + C
    HCa = Ca + H
    NRnFYFAr = Ar + F + Y + F + Rn + N
    NRnMgAr = Ar + Mg + Rn + N
    NTh = Th + N
    OB = B + O
    ORnFAr = Ar + F + Rn + O
    BF = F + B
    TiMg = Mg + Ti
    CRnFAr = Ar + F + Rn + C
    HSi = Si + H
    CRnFYFAr = Ar + F + Y + F + Rn + C
    CRnMgAr = Ar + Mg + Rn + C
    HP = P + H
    NRnFAr = Ar + F + Rn + N
    OTi = Ti + O
    CaP = P + Ca
    PTi = Ti + P
    SiRnFAr = Ar + F + Rn + Si
    CaSi = Si + Ca
    ThCa = Ca + Th
    BP = P + B
    TiTi = Ti + Ti
    HF = F + H
    NAl = Al + N
    OMg = Mg + O

    Atom = Al | Ar | B | C | Ca | F | H | Mg | N | O | P | Rn | Si | Th | Ti | Y | e
    Production = ThF | ThRnFAr | BCa | TiB | TiRnFAr | CaCa | PB | PRnFAr | SiRnFYFAr | SiRnMgAr | SiTh | CaF | PMg | SiAl | CRnAlAr | CRnFYFYFAr | CRnFYMgAr | CRnMgYFAr | HCa | NRnFYFAr | NRnMgAr | NTh | OB | ORnFAr | BF | TiMg | CRnFAr | HSi | CRnFYFAr | CRnMgAr | HP | NRnFAr | OTi | CaP | PTi | SiRnFAr | CaSi | ThCa | BP | TiTi | HF | NAl | OMg
    Phrase = List(Atom | Production, "")

    START = Phrase


# parse_tree = ReverseParser.parse("".join(reversed("CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr")))
# parse_tree = Parser.parse("ab")
parse_tree = Parser.parse("CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr")
print(parse_tree)
print(Parser.repr_parse_tree(parse_tree))

# print(l.parse("CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr"))
