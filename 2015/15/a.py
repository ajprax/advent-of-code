from utils import *


def parse_line(line):
    ingredient, properties = split(line, ": ")
    properties = split(properties, ", ", None).dict()
    properties = properties.map_values(int)
    properties.pop("calories")
    return properties.list().sorted().map(itemgetter(1))


def allocations(n, m):
    return (
        Range(m)
        .product(repeat=n)
        .filter(lambda a: sum(a) == 100)
        .map(np.array)
    )


def score(ingredients, allocation):
    return np.product(np.clip(ingredients.T.dot(allocation.T), 0, inf))


def solve(input):
    ingredients = np.array(split(input, "\n").map(parse_line))
    ningredients, nproperties = ingredients.shape
    return allocations(ningredients, 100).map(lambda allocation: score(ingredients, allocation)).max()


with print_duration():
    print("solution:", solve(read("input.txt")))
