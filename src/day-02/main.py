from math import log10, ceil
from itertools import cycle, chain
from functools import lru_cache


EXAMPLE = 'example.txt'
REAL = 'input.txt.bak'


def parse_ranges(path: str) -> tuple[tuple[int, int]]:
    with open(path, 'r') as fp:
        txt = fp.read()
    ranges = []
    for this in txt.strip().split(','):
        ranges.append(
            tuple(int(x) for x in this.split('-'))
        )
    return tuple(ranges)


@lru_cache
def num_digits(x: int) -> int:
    try:
        return int(log10(x)) + 1 
    except ValueError:
        if x == 0:
            return 1
        raise
    

def repeat(template: int, num_times: int) -> int:
    factor = 10**num_digits(template)
    result = template
    for _ in range(1, num_times):
        result = result*factor + template
    return result


def next_larger_invalid_id(x: int, n: int) -> int:
    """Return the next integer larger than x that is composed of a pattern which repeats n times"""
    nx = num_digits(x)
    np, rem = divmod(nx, n)
    if rem:
        # the input number does not divide into n parts evenly, the next pattern that can create an invalid ID with
        #   n parts must have an extra digit
        pattern = 10**np
    else:
        # the input number divides into n parts evenly, take the first digits as the patter
        pattern = x // 10 ** (nx - np)

    y = repeat(pattern, n)
    if y <= x: 
        y = repeat(pattern + 1, n)

    # print(f'{x=}, {n=}, {nx=}, {np=}, {pattern=}, {y=}')

    return y


def part_1(ranges: tuple[tuple[int, int]]):
    """Return sum of invalid IDs in all input ranges
    IDs are invalid if they consist of the same integer repeated 2x
    """
    total = 0
    for first, last in ranges:

        current = first - 1
        
        while (current := next_larger_invalid_id(current, 2)) <= last:
            total += current
    
    return total


if __name__ == '__main__':

    ranges = parse_ranges(REAL)
    # ranges = parse_ranges(EXAMPLE)
    print(f'Part 1: {part_1(ranges)}')
