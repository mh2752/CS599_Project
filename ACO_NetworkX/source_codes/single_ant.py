# The single_ant class required for the
# ACO algorithm:

import numpy as np


class SingleAnt:
    # Tour-length variable:
    tour_length = 0
    # memory of partial-tour:
    tour = []
    # visited cities:
    visited = []

    def __init__(self, n):
        self.tour_length = 0
        self.tour = np.repeat(None, n + 1)
        self.visited = np.repeat(False, n)

