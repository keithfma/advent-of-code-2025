from math import log10
from functools import lru_cache


EXAMPLE = 'example.txt'
REAL = 'input.txt'


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


def next_value_with_n_repeats(x: int, n: int) -> int:
    """Return the next integer larger than x that is composed of a pattern which repeats n times"""
    nx = num_digits(x)
    np, rem = divmod(nx, n)
    if rem:
        # the input number does not divide into n parts evenly, the next pattern that can create an invalid ID with
        #   n parts must have an extra digit
        pattern = 10**np
    else:
        # the input number divides into n parts evenly, take the first digits as the pattern
        pattern = x // 10 ** (nx - np)

    y = repeat(pattern, n)
    if y <= x: 
        y = repeat(pattern + 1, n)

    return y


def next_value_with_at_least_2_repeats(x: int) -> int:
    """Return the next integer larger than x that is composed of a pattern which repeats >=2 times"""
    result = float('inf')    
    for n in range(2, num_digits(x) + 2):  # minimum of 2 repeats, maximum of num_digits + 1
        result = min(result, next_value_with_n_repeats(x, n))
    return result


def part_1(ranges: tuple[tuple[int, int]]):
    """Return sum of invalid IDs in all input ranges
    IDs are invalid if they consist of the same integer repeated 2x
    """
    total = 0
    for first, last in ranges:
        current = first - 1
        while (current := next_value_with_n_repeats(current, n=2)) <= last:
            total += current
    return total


def part_2(ranges: tuple[tuple[int, int]]):
    """Return sum of invalid IDs in all input ranges
    IDs are invalid if they consist of the same integer repeated *at least* 2x
    """
    total = 0
    for first, last in ranges:
        current = first - 1
        while (current := next_value_with_at_least_2_repeats(current)) <= last:
            total += current
    return total
    

if __name__ == '__main__':

    # ranges = parse_ranges(EXAMPLE)
    ranges = parse_ranges(REAL)
    print(f'Part 1: {part_1(ranges)}')
    print(f'Part 2: {part_2(ranges)}')
