from utils import *


def compare(attribute, operator, value):
    def test(part):
        pvalue = part[attribute]
        if operator == ">":
            return pvalue > value
        elif operator == "<":
            return pvalue < value
        assert False
    return test


def parse_instruction(instruction):
    if "<" in instruction or ">" in instruction:
        attribute = instruction[0]
        operator = instruction[1]
        value, destination = instruction[2:].split(":")
        value = int(value)
        return compare(attribute, operator, value), destination
    else:
        destination = instruction
        return true, destination


def parse_workflow(line):
    open_brace = line.index("{")
    name = line[:open_brace]
    instructions = fit(line[open_brace+1:-1].split(",")).map(parse_instruction)
    return name, instructions


def parse_workflows(lines):
    return lines.map(parse_workflow).dict()


def parse_attribute(attr):
    name, value = attr.split("=")
    return name, int(value)


def parse_part(line):
    return fit(line[1:-1].split(",")).map(parse_attribute).dict()


def parse_parts(lines):
    return lines.map(parse_part)


def process(workflows, parts):
    accepted = List()
    for part in parts:
        workflow = workflows["in"]
        while workflow:
            for test, destination in workflow:
                if test(part):
                    match destination:
                        case "A":
                            accepted.append(part)
                            workflow = None
                            break
                        case "R":
                            workflow = None
                            break
                        case next_workflow:
                            workflow = workflows[next_workflow]
                            break
            else:
                break
    return accepted


def score(accepted_parts):
    return accepted_parts.flat_map(lambda part: part.values()).reduce(add)


def solve(input):
    workflows, parts = split(input, "\n\n")
    workflows = parse_workflows(fit(workflows.split("\n")))
    parts = parse_parts(fit(parts.split("\n")))
    return score(process(workflows, parts))


with print_duration():
    print("solution:", solve(read("input.txt")))
