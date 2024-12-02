from hashlib import md5

from utils import *


def hash(s):
    return md5(s.encode("ascii")).hexdigest()


def solve(input):
    return Iterator(count()).first(lambda i: hash(input + str(i)).startswith("00000"))


with print_duration():
    print("solution:", solve(read("input.txt")))
