
EXAMPLE = 'example.txt'
REAL = 'input.txt'


type Range = tuple[int, int]


def parse(path) -> tuple[list[Range], list[int]]:
    
    with open(path, 'r') as f:

        ranges = []
        ids = []
        for line in f.readlines():
            txt = line.strip()
            if txt:
                try:
                    print(txt.split('-'))
                    a, b = txt.split('-')
                    ranges.append((int(a), int(b)))
                except Exception:
                    ids.append(int(txt))

    return ranges, ids


def consolidate(ranges: list[Range]) -> list[Range]:
    """Return a list of consolidated, non-overlapping ranges sorted from low to high"""
    ranges = sorted(ranges)

    done: list[Range] = []
    cur = ranges[0]
    for nxt in ranges[1:]:
        # check if intersecting, because the list of ranges is sorted we know cur starts before nxt,
        #   and so only check if nxt begins before curr ends
        if nxt[0] <= cur[1]:
            cur = (cur[0], max(cur[1], nxt[1]))
        else:
            done.append(cur)
            cur = nxt
    done.append(cur)
    
    return done


def count_fresh(ranges: list[Range], ids: list[int]) -> int:
    """Count the number of fresh ids (i.e., ids that are within any range
    
    Approach is to consolidate and sort the ranges and sort the ids, then march forward
        over both lists together to find ids that are in ranges without always looping over all ranges.

    This is needlessly fancy, but fun!
    """

    ranges = consolidate(ranges)
    ranges.reverse() # largest range is first, so we can pop from small to large
    ids.sort()
    ids.reverse()

    count = 0
    r = ranges.pop()
    i = ids.pop()

    while True:

        try:
            if i > r[1]:
                # id is above this range, but might be "fresh" in a larger range
                # move on to the next large range
                r = ranges.pop()

            elif r[0] <= i <= r[1]:
                # fresh! move on to the next id
                count += 1
                i = ids.pop()
            
            elif i < r[0]:
                # not fresh. id is below this range, and must be above all others because we iterated in order
                # move on to next id
                i = ids.pop()
            
            else:
                raise ValueError("I don't think this is possible")

        except IndexError:
            # exhaused either ranges or ids, so we have found all the fresh ids and are done
            break

    return count


if __name__ == '__main__':

    ranges, ids = parse(EXAMPLE)
    ranges, ids = parse(REAL)
    print(f'Part 1: {count_fresh(ranges, ids)}')