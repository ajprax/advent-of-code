from utils import *


def parse_line(line):
    ingredient, stats = split(line, ": ")
    stats = split(stats, ", ", None).dict()
    stats = stats.map_values(int)
    return stats.list().sorted().map(itemgetter(1))


def matches_calorie_count(calories, calorie_count):
    def test(allocation):
        return sum(calories * allocation) == calorie_count
    return test


def allocations(n, m, calories, calorie_count):
    return (
        Range(m)
        .product(repeat=n)
        .filter(lambda a: sum(a) == 100)
        .filter(matches_calorie_count(calories, calorie_count))
        .map(np.array)
    )


def score(ingredients, allocation):
    return np.product(np.clip(ingredients.T.dot(allocation.T), 0, inf))


def solve(input):
    ingredients = np.array(split(input, "\n").map(parse_line))
    calories = ingredients[:, 0]
    ingredients = ingredients[:, 1:]
    ningredients, nproperties = ingredients.shape
    return allocations(ningredients, 100, calories, 500).map(lambda allocation: score(ingredients, allocation)).max()


with print_duration():
    print("solution:", solve(read("input.txt")))
