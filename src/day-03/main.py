
EXAMPLE = 'example.txt'
REAL = 'input.txt'


def parse_banks(path: str) -> tuple[str, ...]:
    banks = []
    with open(path, 'r') as fp:
        for line in fp.readlines():
            banks.append(line.strip())
    return banks


# character with a unicode point value < that of '0', used to indicate None
# while allowing use of comparison operators
NOTHING = '.'  

def max_joltage_2(bank: str) -> int:
    """Return maximum integer that can be formed by selecting two character in the input string"""
    a = b = NOTHING
    last_idx = len(bank) - 1
    for i, x in enumerate(bank):
        if x > a and i != last_idx:
            # a new highest digit for the 10s place
            a = x
            b = NOTHING
        elif x > b:
            # a new highest digit for the 1s place
            b = x
    return int(a + b)

def part_1(banks: tuple[str, ...]) -> int:
    return sum(max_joltage_2(b) for b in banks)


def max_joltage_12(bank: str) -> int:
    """Return maximum integer that can be formed by selecting TWELVE characters in the input string"""

    selected = []
    start = 0
    end = len(bank)

    for rem in range(12, 0, -1):
        # find the highest value in the subset of the bank that still leaves enough batteries to fill the remaining slots
        end = len(bank) - rem + 1
        value = max(bank[start:end])
        selected.append(value)
        # select the battery after the selected one as the start point for filling remaining slots
        start = bank.index(value, start) + 1
    
    return int(''.join(selected))


def part_2(banks: tuple[str, ...]) -> int:
    return sum(max_joltage_12(b) for b in banks)


if __name__ == '__main__':

    banks = parse_banks(EXAMPLE)
    banks = parse_banks(REAL)
    print(f'Part 1: {part_1(banks)}')
    print(f'Part 2: {part_2(banks)}')
