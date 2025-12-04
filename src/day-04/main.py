import numpy as np
from dataclasses import dataclass


EXAMPLE = 'example.txt'
REAL = 'input.txt'


def parse_grid(path: str) -> np.ndarray:
    grid = []
    with open(path, 'r') as fp:
        for line in fp.readlines():
            grid.append([x == '@' for x in line.strip()])
    return np.array(grid, dtype=np.uint8)  # uint8 uses same storage as bool, but displays better for debugging


def count_accessible_rolls(grid: np.ndarray) -> int:
    # pad the input array, so we never have to worry about edges
    grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)

    # loop over all interior points, and check the neighborhood around them by summing
    count = 0
    for ii in range(1, grid.shape[0]-1):
        for jj in range(1, grid.shape[1]-1):
            if grid[ii, jj]: 
                # there is a roll here, check if it is accessible
                num_neighbors = np.sum(grid[ii-1:ii+2, jj-1:jj+2])
                if num_neighbors < 5:  # four neighbors and the roll itself 
                    count += 1
    
    return count


def remove_rolls(grid: np.ndarray) -> int:

    # pad the input array, so we don't have to worry about edges
    grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)

    # populate the list of positions to check, which is all interior points to begin with
    candidates: set[tuple[int, int]] = set()
    for ii in range(1, grid.shape[0]-1):
        for jj in range(1, grid.shape[1]-1):
            candidates.add((ii, jj))

    # check positions until there are no more
    count = 0
    while candidates:
        ii, jj = candidates.pop()

        if grid[ii, jj] == 0:
            continue  # no roll to remove 

        num_neighbors = np.sum(grid[ii-1:ii+2, jj-1:jj+2])
        if num_neighbors > 4: 
            # inaccessible, 3 neighbors and the roll itself 
            continue

        # remove the roll, count it, and mark all neighbors as candidates
        grid[ii, jj] = 0
        count += 1
        for di in range(-1, 2):
            for dj in range(-1, 2):
                loc = (ii+di, jj+dj)
                if (
                    loc[0] != (ii, jj)  # skip self
                    or loc[0] == 0 or loc[0] == grid.shape[0] - 1   # skip pad
                    or loc[1] < 1 or loc[1] == grid.shape[1] -1  # skip pad
                ):
                    candidates.add(loc)

    return count

if __name__ == '__main__':

    grid = parse_grid(EXAMPLE)
    grid = parse_grid(REAL)
    print(f'Part 1: {count_accessible_rolls(grid)}')
    print(f'Part 2: {remove_rolls(grid)}')
