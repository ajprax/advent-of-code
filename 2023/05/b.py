from utils import *


# make each map two dense lists: one of input ranges, one output ranges
def parse_map_lines(lines):
    ranges = (
        split(lines, "\n")[1:]
        .map(lambda line: split(line, None).map(int))
        .sorted(itemgetter(1))
        .map(t(lambda dst, src, length: (range(src, src + length), range(dst, dst + length))))
    )
    # fill gaps between src ranges
    for i in range(len(ranges) - 2, -1, -1):
        stop = ranges[i][0].stop
        start = ranges[i+1][0].start
        if start != stop:
            ranges.insert(i + 1, (range(stop, start), range(stop, start)))
    # ensure we're dense to 0
    if ranges[0][0].start != 0:
        ranges.insert(0, (range(0, ranges[0][0].start), range(0, ranges[0][0].start)))
    # and max (2**32)
    if ranges[-1][0].stop != 2**32:
        ranges.append((range(ranges[-1][0].stop, 2**32), range(ranges[-1][0].stop, 2**32)))
    return ranges.unzip()


def collapse(a, b):
    # collapse (asrc, adst), (bsrc, bdst) to (asrc, bdst), splitting as necessary
    asrc, adst = a
    bsrc, bdst = b

    out = List()
    for ai in range(len(adst)):
        for bi in range(len(bsrc)):
            a = adst[ai]
            b = bsrc[bi]
            if ranges_intersect(a, b):
                astart = max(0, b.start - a.start)
                if a.stop < b.stop:
                    astop = min(len(a), a.stop - a.start + astart)
                else:
                    astop = min(len(a), a.stop - a.start + astart - (a.stop - b.stop))

                bstart = max(0, a.start - b.start)
                bstop = bstart + (astop - astart)

                out.append((
                    range(asrc[ai].start + astart, asrc[ai].start + astop),
                    range(bdst[bi].start + bstart, bdst[bi].start + bstop)
                ))

    return out.unzip()


def solve(input):
    seeds, *maps = split(input, "\n\n")
    seeds = (
        fit(seeds.split(": ")[1].split())
        .map(int)
        .batch(2)
        .map(t(lambda start, length: (range(start, start + length), range(start, start + length))))
        .unzip()
    )
    return List(maps).map(parse_map_lines).fold(seeds, collapse)[1].map(lambda b: b.start).min()


with print_duration():
    print("solution:", solve(read("sample.txt")), "expected:", 46)


with print_duration():
    print("solution:", solve(read("input.txt")))
