from utils import *

def solve(input):

    molecule = input.split('\n')[-1][::-1]

    reps = {
        m[1][::-1]: m[0][::-1]
        for m in re.findall(r'(\w+) => (\w+)', input)
    }

    def rep(x):
        return reps[x.group()]

    count = 0
    while molecule != 'e':
        molecule = re.sub('|'.join(reps.keys()), rep, molecule, 1)
        count += 1
    return count

with print_duration():
    print("solution:", solve(read("input.txt")))
