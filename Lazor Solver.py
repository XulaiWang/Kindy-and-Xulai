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

def solve(self):
        """ Try all possible block placement combinations """

        self.empty_spaces = [(x * 2 + 1, y * 2 + 1) for y in range(len(self.grid)) for x in range(len(self.grid[0])) if
                             self.grid[y][x] == "o"]

        block_types = ['A'] * self.blocks['A'] + ['B'] * self.blocks['B'] + ['C'] * self.blocks['C']

        occupied_spaces = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != 'x' and self.grid[i][j] != 'o':
                    occupied_spaces[(j * 2 + 1, i * 2 + 1)] = self.grid[i][j]

        self.dfs(0, self.blocks['A'] + self.blocks['B'] + self.blocks['C'], [])
        print("Block placement combinations generated")

        unique_types = []
        s = set()
        for bb in itertools.permutations(block_types):
            p = tuple(bb)
            if p not in s:
                s.add(p)
                unique_types.append(bb)

        for bb in unique_types:
            for placement in self.vecs:
                placed_blocks = {placement[i]: bb[i] for i in range(len(bb))}
                for x, y in occupied_spaces:
                    placed_blocks[(x, y)] = occupied_spaces[(x, y)]
                if all(target in self.simulate_lasers(self.to_hashable(placed_blocks)) for target in self.targets):
                    self.draw_grid(len(self.grid), len(self.grid[0]), placed_blocks)
                    return placed_blocks

        return None

 def draw_grid(self, n, m, colored_cells):
        fig, ax = plt.subplots(figsize=(m, n))
        ax.set_aspect('equal')
        plt.axis('off')

        cell_width = 1.0
        cell_height = 1.0

        for i in range(n + 1):
            ax.plot([0, m], [i, i], color='black', lw=1)
        for j in range(m + 1):
            ax.plot([j, j], [0, n], color='black', lw=1)

        for (row, col) in colored_cells:
            c = colored_cells[(row, col)]
            row = (row - 1) / 2
            col = (col - 1) / 2
            x = row
            y = n - col - 1

            if c == 'A':
                rect = patches.Rectangle(
                    (x, y), cell_width, cell_height,
                    edgecolor='black', facecolor='#ffa500', alpha=1)
            elif c == 'B':
                rect = patches.Rectangle(
                    (x, y), cell_width, cell_height,
                    edgecolor='black', facecolor='black', alpha=1)
            elif c == 'C':
                rect = patches.Rectangle(
                    (x, y), cell_width, cell_height,
                    edgecolor='black', facecolor='#00bfff', alpha=1)
            ax.add_patch(rect)
