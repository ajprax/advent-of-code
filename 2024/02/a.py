from utils import *


def is_safe(report):
    differences = report.sliding(2).map(t(sub))
    increasing = differences.all(lambda d: d > 0)
    decreasing = differences.all(lambda d: d < 0)
    one_to_three = differences.map(abs).all(lambda d: 1 <= d <= 3)
    return (increasing or decreasing) and one_to_three


def solve(input):
    reports = split(input, "\n", " ").map(lambda report: report.map(int))
    return reports.filter(is_safe).size()


with print_duration():
    print("solution:", solve(read("input.txt")))
