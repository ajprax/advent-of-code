from utils import *


def parse_instruction(instruction):
    if "<" in instruction or ">" in instruction:
        attribute = "xmas".index(instruction[0])
        operator = instruction[1]
        value, destination = instruction[2:].split(":")
        value = int(value)
        return (attribute, operator, value), destination
    else:
        destination = instruction
        return (None, None, None), destination


def parse_workflow(line):
    open_brace = line.index("{")
    name = line[:open_brace]
    instructions = fit(line[open_brace+1:-1].split(",")).map(parse_instruction)
    return name, instructions


def parse_workflows(lines):
    return lines.map(parse_workflow).dict()


def split_parts(ranges, attribute, operator, value):
    passing = copy(ranges)
    failing = copy(ranges)
    l, g = split_range(ranges[attribute], value)
    passing[attribute], failing[attribute] = (l, g) if operator == "<" else (g, l)
    return passing, failing


def count_ranges(ranges):
    return fit(ranges).map(len).reduce(mul)


def solve(input):
    workflows, parts = split(input, "\n\n")
    workflows = parse_workflows(fit(workflows.split("\n")))

    accepted = 0
    rejected = 0
    # (workflow name, instruction index, ranges of parts that made it here)
    search = [("in", 0, [range(1, 4001) for _ in range(4)])]
    while search:
        workflow_name, i, ranges = search.pop()
        workflow = workflows[workflow_name]
        assert i < len(workflow)
        ((attribute, operator, value), destination) = workflow[i]
        match operator:
            case None:
                if destination == "A":
                    accepted += count_ranges(ranges)
                elif destination == "R":
                    rejected += count_ranges(ranges)
                else:
                    search.append((destination, 0, ranges))
            case "<":
                passing, failing = split_parts(ranges, attribute, operator, value)
                if destination == "A":
                    accepted += count_ranges(passing)
                elif destination == "R":
                    rejected += count_ranges(passing)
                else:
                    search.append((destination, 0, passing))
                search.append((workflow_name, i + 1, failing))
            case ">":
                passing, failing = split_parts(ranges, attribute, operator, value)
                if destination == "A":
                    accepted += count_ranges(passing)
                elif destination == "R":
                    rejected += count_ranges(passing)
                else:
                    search.append((destination, 0, passing))
                search.append((workflow_name, i + 1, failing))
            case unknown:
                assert False, unknown
    assert accepted + rejected == 4000**4
    return accepted


with print_duration():
    print("solution:", solve(read("input.txt")))
