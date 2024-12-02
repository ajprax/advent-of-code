from hashlib import md5
from multiprocessing import Pool

from utils import *


def hash(s):
    return md5(s.encode("ascii")).hexdigest()


def search(args):
    input, start, end, step = args
    for i in range(start, end, step):
        if hash(input + str(i)).startswith("000000"):
            return i


def solve(input):
    with Pool(10) as pool:
        num = 0
        while True:
            results = List(pool.map(search, [(input, num + i, num + int(10e6), 10) for i in range(10)])).filter()
            if results:
                return results.min()
            num += 10e6


if __name__ == "__main__":
    with print_duration():
        print("solution:", solve(read("input.txt")))
