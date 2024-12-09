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
        return self.id * (self.end - self.start) * ((self.start + self.end - 1) / 2)


def solve(input):
    fragged = deque()
    start = 0
    for id, (flen, glen) in (
        split(input, "")
        .map(int)
        # it's helpful to have an empty gap at the end so the number of files and gaps are equal
        .appended(0)
        .batch(2)
        .enumerate()
    ):
        fragged.append(File(id, start, flen))
        start += flen
        fragged.append(Gap(start, glen))
        start += glen

    defragged = List()
    # the first item is a file and this avoids the need to handle the empty defragged case in the loop
    defragged.append(fragged.popleft())

    while fragged:
        chunk = fragged.popleft()
        if chunk.is_file():
            chunk.start = defragged[-1].end
            defragged.append(chunk)
        else:
            while chunk:
                if fragged[-1].is_gap():
                    fragged.pop()
                if len(fragged[-1]) <= len(chunk):
                    file = fragged.pop()
                    file.start = defragged[-1].end
                    defragged.append(file)
                    chunk.len -= len(file)
                else:
                    fragged[-1].len -= len(chunk)
                    defragged.append(File(fragged[-1].id, defragged[-1].end, len(chunk)))
                    chunk.len = 0

    return defragged.map(lambda f: f.checksum).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
