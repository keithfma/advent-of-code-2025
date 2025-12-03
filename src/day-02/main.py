from math import log10

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


def invalid_ids_in_range(first: int, last: int) -> int:
    """Return sum of invalid IDs in the range first->last inclusive"""
    assert first < last and first > 0

    invalid = 0
    current = first
    while current <= last:
        
        num_digits = int(log10(current)) + 1 
        print(f'{current=}, {num_digits=}', end='')
        
        if num_digits % 2:
            # no invalid ID has an odd number of digits, advance to the next value with 
            #   an even number of digits
            current = 10**(num_digits)
            print(f' -> {current=}')
            continue

        factor = 10**(num_digits // 2)  # already know it's even 
        left = current // factor
        right = current - left*factor
        print(f', {left=}, {right=}', end='')

        if left == right:
            # found one! increment the counter
            invalid += current
            print(f' -> INVALID -> ', end='')
        else:
            print(f' -> VALID -> ', end='')


        if left <= right:
            # advance to next possible invalid ID by incrementing the left value and zeroing the right
            left += 1
            right = 0
        
        else:
            # advance to next possible invalid ID by making the right equal to the left
            right = left
        

        # recombine (modified) left and right sides
        current = left*factor + right
        print(f'{left=}, {right=}, {current=}')
    
    return invalid


if __name__ == '__main__':

    ranges = parse_ranges(REAL)
    print(f'Part 1: {sum(invalid_ids_in_range(*r) for r in ranges)}')
