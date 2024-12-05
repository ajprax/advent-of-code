from utils import *


def drop(report, i):
    report = report.copy()
    report.pop(i)
    return report


def is_safe(report):
    differences = report.sliding(2).map(t(sub))
    increasing = differences.all(lambda d: d > 0)
    decreasing = differences.all(lambda d: d < 0)
    one_to_three = differences.map(abs).all(lambda d: 1 <= d <= 3)
    return (increasing or decreasing) and one_to_three


def is_dampened_safe(report):
    return is_safe(report) or any(is_safe(drop(report, i)) for i in range(len(report)))


def solve(input):
    reports = split(input, "\n", " ").map(lambda report: report.map(int))
    return reports.filter(is_dampened_safe).size()


with print_duration():
    print("solution:", solve(read("input.txt")))
