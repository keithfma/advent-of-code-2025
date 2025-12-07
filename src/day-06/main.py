import numpy as np



EXAMPLE = 'example.txt'
REAL = 'input.txt'

OPERATION_MAP: dict[str, np.ufunc] = {'+': np.add, '*': np.multiply}


def do_some_kids_homework(path: str) -> tuple[np.ndarray, list[np.ufunc]]:
    with open(path, 'r') as f:
        lines = f.readlines()
    
    nums = []
    for line in lines[:-1]:
        nums.append([int(x) for x in line.strip().split()])
    nums = np.array(nums)

    ops = [OPERATION_MAP[x] for x in lines[-1].strip().split()]

    total = 0
    for idx in range(len(ops)):
        total += ops[idx].reduce(nums[:, idx])

    return total


def do_some_kids_homework_correctly(path: str) -> tuple[np.ndarray, list[np.ufunc]]:
    with open(path, 'r') as f:
        lines = [x.rstrip('\n') for x in f.readlines()]

    # transpose the lines with numbers in them to get the "problems", which are sequences of ints
    problems = []
    problem = []
    for digits in zip(*lines[:-1]):
        try:
            problem.append( int(''.join(digits)) )
        except ValueError:
            # next problem!
            problems.append(problem)
            problem = []
    # don't forget the last one
    problems.append(problem)
    
    ops = [OPERATION_MAP[x] for x in lines[-1].strip().split()]

    total = 0
    for problem, op in zip(problems, ops):
        total += op.reduce(problem)
    
    return int(total)
    

if __name__ == '__main__':

    print(f'Part 1: {do_some_kids_homework(REAL)}')
    print(f'Part 2: {do_some_kids_homework_correctly(REAL)}')