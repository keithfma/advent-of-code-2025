import numpy as np


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
                neighborhood = grid[ii-1:ii+2, jj-1:jj+2]
                num_neighbors = np.sum(neighborhood)
                if num_neighbors < 5:  # four neighbors and the roll itself 
                    count += 1
    
    return count


if __name__ == '__main__':

    # grid = parse_grid(EXAMPLE)
    grid = parse_grid(REAL)
    print(f'Part 1: {count_accessible_rolls(grid)}')
