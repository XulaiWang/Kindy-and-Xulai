***
* Lazor Project 2025 by Kindy Gan and Xulai Wang from softwawre carpentry


import itertools
from functools import lru_cache
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from configs import DefaultConfig

configs = DefaultConfig()


class LazorSolver:
    def __init__(self, filename):
        self.grid = []
        self.lasers = []
        self.targets = []
        self.blocks = {'A': 0, 'B': 0, 'C': 0}
        self.vecs = []
        self.load_bff(filename)
        self.empty_spaces = []

    def load_bff(self, filename):
        """ Parse .bff file """
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        reading_grid = False
        grid_data = []
        for line in lines:
            if line == "GRID START":
                reading_grid = True
            elif line == "GRID STOP":
                reading_grid = False
                self.grid = grid_data
            elif reading_grid:
                grid_data.append(line.split())

            elif line.startswith("L "):
                line = line[2:]
                x, y, dx, dy = map(int, line.split())
                self.lasers.append(((x, y), (dx, dy)))

            elif line.startswith("P "):
                line = line[2:]
                x, y = map(int, line.split())
                self.targets.append((x, y))

            elif line.startswith("A ") or line.startswith("B ") or line.startswith("C "):
                block_type, count = line.split()
                self.blocks[block_type] = int(count)
        print("bff file parsed successfully")

    def to_hashable(self, placed_blocks):
        return tuple(sorted(placed_blocks.items()))

 @lru_cache(maxsize=None)
    def simulate_lasers(self, placed_blocks_hash):
        placed_blocks = dict(placed_blocks_hash)
        """ Simulate laser paths, return visited points """
        visited = set()  # Record points visited by lasers
        seen_lasers = set()  # Track already simulated paths to avoid infinite loops
        active_lasers = list(self.lasers)

        while active_lasers:
            (x, y), (dx, dy) = active_lasers.pop(0)

            while 0 <= x <= 2 * len(self.grid[0]) and 0 <= y <= 2 * len(self.grid):
                # Record visited point and direction to prevent repeats
                if (x, y, dx, dy) in seen_lasers:
                    break
                seen_lasers.add((x, y, dx, dy))

                visited.add((x, y))

                # **Check if hitting a block**
                if (x + dx, y) in placed_blocks:
                    block = placed_blocks[(x + dx, y)]

                    if block == "A":  # Reflect
                        dx = -dx  # Only reverse x direction
                        active_lasers.append(((x, y), (dx, dy)))
                        break
                    elif block == "B":  # Absorb (terminate)
                        break
                    elif block == "C":  # Refract
                        active_lasers.append(((x, y), (-dx, dy)))  # Add refracted beam
                        x, y = x + dx, y + dy

                elif (x, y + dy) in placed_blocks:
                    block = placed_blocks[(x, y + dy)]

                    if block == "A":  # Reflect
                        dy = -dy  # Only reverse y direction
                        active_lasers.append(((x, y), (dx, dy)))
                        break
                    elif block == "B":  # Absorb (terminate)
                        break
                    elif block == "C":  # Refract
                        active_lasers.append(((x, y), (dx, -dy)))  # Add refracted beam
                        x, y = x + dx, y + dy

                # **Move beam**
                else:
                    x, y = x + dx, y + dy
        return visited

    def dfs(self, cur, to, vec):
        """
        Generate all combinations (element order irrelevant)
        :param cur: current start index
        :param to: number of elements to select
        :param vec: current path
        """
        if len(vec) == to:
            self.vecs.append(vec.copy())
            return
        if cur >= len(self.empty_spaces):
            return

        # Select current element
        vec.append(self.empty_spaces[cur])
        self.dfs(cur + 1, to, vec)
        vec.pop()

        # Do not select current element
        self.dfs(cur + 1, to, vec)
