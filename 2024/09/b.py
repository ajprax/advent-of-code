from utils import *


@dataclass
class Gap:
    start: int
    len: int

    def __bool__(self):
        return bool(self.len)

    def __len__(self):
        return self.len

    @property
    def end(self):
        return self.start + self.len

    def is_file(self):
        return False

    def is_gap(self):
        return True


@dataclass
class File:
    id: int
    start: int
    len: int

    def __bool__(self):
        return bool(self.len)

    def __len__(self):
        return self.len

    @property
    def end(self):
        return self.start + self.len

    def is_file(self):
        return True

    def is_gap(self):
        return False

    @property
    def checksum(self):
        return int(self.id * (self.end - self.start) * ((self.start + self.end - 1) / 2))


def solve(input):
    chunks = List()

    start = 0
    for id, (flen, glen) in (
        split(input, "")
        .map(int)
        # it's helpful to have an empty gap at the end so the number of files and gaps are equal
        .appended(0)
        .batch(2)
        .enumerate()
    ):
        chunks.append(File(id, start, flen))
        start += flen
        chunks.append(Gap(start, glen))
        start += glen

    for i in range(len(chunks) - 2, -1, -2):
        file = chunks[i]
        for j in range(1, i, 2):
            gap = chunks[j]
            if len(file) <= len(gap):
                # we don't have to move the file in the list, just "on disk"
                file.start = gap.start
                gap.start += len(file)
                gap.len -= len(file)
                break

    return chunks.filter(lambda c: c.is_file()).map(lambda f: f.checksum).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
