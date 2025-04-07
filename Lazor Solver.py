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


