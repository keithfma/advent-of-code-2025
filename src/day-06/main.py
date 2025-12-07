import numpy as np



EXAMPLE = 'example.txt'
REAL = 'input.txt'

OPERATION_MAP: dict[str, np.ufunc] = {'+': np.add, '*': np.multiply}


def parse(path: str) -> tuple[np.ndarray, list[np.ufunc]]:
    with open(path, 'r') as f:
        lines = f.readlines()
    
    nums = []
    for line in lines[:-1]:
        nums.append([int(x) for x in line.strip().split()])
    nums = np.array(nums)

    ops = [OPERATION_MAP[x] for x in lines[-1].strip().split()]

    return nums, ops


def do_some_kids_homework(nums: np.ndarray, ops: np.ufunc):
    total = 0
    for idx in range(len(ops)):
        total += ops[idx].reduce(nums[:, idx])
    return total



if __name__ == '__main__':

    # numbers, operators = parse(EXAMPLE)
    numbers, operators = parse(REAL)
    print(f'Part 1: {do_some_kids_homework(numbers, operators)}')