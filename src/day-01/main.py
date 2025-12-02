from math import floor, copysign, trunc


def load_instructions(path) -> list[int]:
    out = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            direction = line[0]
            value = int(line[1:])
            if direction == 'L':
                value = -value
            elif direction == 'R':
                pass
            else: 
                raise ValueError
            out.append(value)
    return out


def follow_instructions_part_1(values: list[int]) -> int:
    """Return number of times the dial lands on 0"""
    num_zeros = 0
    dial = 50
    for value in values:
        dial += value
        if dial % 100 == 0:
            num_zeros += 1
    return num_zeros


def follow_instructions_part_2(values: list[int]) -> int:
    """Return number of times the dial touches 0"""
    dial = 50
    num_zeros = 0
    for value in values:
        sign = copysign(1, value)
        for _ in range(abs(value)):
            dial += sign
            if dial % 100 == 0:
                num_zeros += 1
    return num_zeros

if __name__ == '__main__':

    # instr = load_instructions('example.txt')
    instr = load_instructions('input.txt')

    part_1 = follow_instructions_part_1(instr)
    print(f'{part_1=}')

    part_2 = follow_instructions_part_2(instr)
    print(f'{part_2=}')
