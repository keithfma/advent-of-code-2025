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


def invalid_ids_in_range(first: int, last: int) -> list[int]:
    assert first < last and first > 0

    invalid = 0
    all = []
    current = first
    while current <= last:
        
        num_digits = int(log10(current)) + 1 
        # print(f'{current=}, {num_digits=}', end='')
        
        if num_digits % 2:
            # no invalid ID has an odd number of digits, advance to the next value with 
            #   an even number of digits
            current = 10**(num_digits)
            # print(f' -> {current=}')
            continue

        factor = 10**(num_digits // 2)  # already know it's even 
        left = current // factor
        right = current - left*factor
        # print(f', {left=}, {right=}', end='')

        if left == right:
            # found one! increment the counter
            all.append(current)
            invalid += current
            # print(f' -> INVALID -> ', end='')
        else:
            # print(f' -> VALID -> ', end='')
            pass


        if left <= right:
            # advance to next possible invalid ID by incrementing the left value and zeroing the right
            left += 1
            right = 0
        
        else:
            # advance to next possible invalid ID by making the right equal to the left
            right = left
        

        # recombine (modified) left and right sides
        current = left*factor + right
        # print(f'{left=}, {right=}, {current=}')
    
    return all




# def next_larger_invalid_id(value: int) -> int:
# 
#     num_digits = int(log10(value)) + 1 
#     
#     print(f'{value=}, {num_digits=}', end='')
# 
#     next_invalid = float('inf')
#     for i in range(1, ceil(num_digits / 2)):
#         digits = cycle(txt[:i])
#         candidate = ''.join(next(digits) for _ in range(num_digits))
#         print(f'{i=}, {candidate=}')


# def crack(x: int, n: int) -> list[int]:
#     factor = 10**n
#     parts = []
#     while x:
#         x, part = divmod(x, factor)
#         parts.append(part)
#     return parts


# def weld(parts: list[int], n: int) -> int:
#     factor = 10**n
#     x = 0
#     for part in reversed(parts):
#         x = x*factor + part
#     return x




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


# def head(x: int, n: int) -> int:
#     nx = num_digits(x)
#     if n > nx:
#         raise ValueError(f'{x=} has fewer than {n=} digits')
#     return x // 10**(nx-n)


# def num_parts(x: int, n: int) -> int:
#     nx = num_digits(x)
#     if n > nx:
#         raise ValueError(f'{x=} has fewer than {n=} digits')
#     return ceil(n / nx)


def _next_larger_invalid_id(x: int, n: int) -> int:
    """Return the next next invalid ID larger than x with a repeating pattern of n digits"""
    nx = num_digits(x)
    num_parts = max(2, ceil(nx / n))
    # TOOD: this ain't quite right. we are grabbing too many digits when the length of the number is odd.
    head = min(x, x // 10 ** (nx - n))

    y = repeat(head, num_parts)
    if y <= x: 
        y = repeat(head + 1, num_parts)

    print(f'{x=}, {n=}, {nx=}, {num_parts=}, {head=}, {y=}')

    return y


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

    print(f'{x=}, {n=}, {nx=}, {np=}, {pattern=}, {y=}')

    return y

# def next_larger_invalid_id(x: int) -> int:
#     """Return the next next invalid ID larger than x with a repeating pattern of n digits"""
#     result = float('inf')
#     nx = num_digits(x)
# 
#     for n in range(1, nx):  # TODO: truncate?
# 
#         num_parts = ceil(nx / n)
#         head = x // 10 ** (nx - n)
# 
#         candidate = repeat(head, num_parts)
#         if candidate <= x: 
#             candidate = repeat(head + 1, num_parts)
# 
#         result = min(candidate, result)
#     
#     return result


def part_1a(ranges: tuple[tuple[int, int]]):
    """OG version, which works"""
    return list(chain(*[invalid_ids_in_range(*r) for r in ranges]))


def part_1b(ranges: tuple[tuple[int, int]]):
    """Return sum of invalid IDs in all input ranges
    IDs are invalid if they consist of the same integer repeated 2x
    """
    total = 0
    all = []
    for first, last in ranges:

        current = first - 1
        
        while True:
            current = next_larger_invalid_id(current, 2)
            if current > last:
                break
            total += current
            all.append(current)
    
    return all


if __name__ == '__main__':

    ranges = parse_ranges(REAL)
    # ranges = parse_ranges(EXAMPLE)
    a = part_1a(ranges)
    b = part_1b(ranges)
    for aa, bb in zip(a, b):
        print(f'{aa=}, {bb=}')
    # print(f'Part 1: {part_1(ranges)}')

    # x = 1000
    # for _ in range(1000):
    #     x = next_larger_invalid_id(x)
    #     print(f'{x=}')

