import numpy as np
from pprint import pprint

EXAMPLE = 'example.txt'
REAL = 'input.txt'


def parse(path) -> tuple[np.ndarray, int]:
    """Return boolean array with splitters as 1 and all other locations as 0, and column index of the start point"""
    rows = []
    with open(path, 'r') as f:
        
        line = f.readline().strip('\n')
        start_index = line.index('S')

        for line in f.readlines():
            rows.append([1 if x == '^' else 0 for x in line.strip('\n')])

    return np.array(rows, dtype=np.uint8), start_index


def count_splits(path) -> int:
    manifold, start = parse(path)
    
    curr_beam = np.zeros((manifold.shape[1],), dtype=np.uint32)
    next_beam = np.zeros((manifold.shape[1],), dtype=np.uint32)
    curr_beam[start] = 1
    count = 0

    for ii in range(manifold.shape[0]):

        for jj in range(manifold.shape[1]):
            if curr_beam[jj]:
                if manifold[ii, jj]:
                    count += 1
                    next_beam[jj-1] = 1
                    next_beam[jj+1] = 1
                else:
                    next_beam[jj] = 1

        # print(f'curr_beam = {curr_beam}')
        # print(f'manifold  = {manifold[ii, :]}')
        # print(f'next_beam = {next_beam}\n')

        curr_beam[:] = next_beam[:]
        next_beam[:] = 0
    
    return count


def count_timelines(path) -> int:
    manifold, start = parse(path)
    
    curr_beam = np.zeros((manifold.shape[1],), dtype=np.uint64)
    next_beam = np.zeros((manifold.shape[1],), dtype=np.uint64)
    curr_beam[start] = 1

    for ii in range(manifold.shape[0]):
        for jj in range(manifold.shape[1]):
            if curr_beam[jj]:
                if manifold[ii, jj]:
                    next_beam[jj-1] += curr_beam[jj]
                    next_beam[jj+1] += curr_beam[jj]
                else:
                    next_beam[jj] += curr_beam[jj]

        # print(f'curr_beam = {curr_beam}')
        # print(f'manifold  = {manifold[ii, :]}')
        # print(f'next_beam = {next_beam}\n')

        curr_beam[:] = next_beam[:]
        next_beam[:] = 0
    
    return np.sum(curr_beam)


if __name__ == '__main__':

    # print(f'Part 1: {count_splits(EXAMPLE)}')
    print(f'Part 1: {count_splits(REAL)}')

    # print(f'Part 2: {count_timelines(EXAMPLE)}')
    print(f'Part 2: {count_timelines(REAL)}')

    # 102 is too low (silent overflow error)
    # 63685577574 is too low (noisy overflow error)
    # 25592971184998 is right. Damn precision.
