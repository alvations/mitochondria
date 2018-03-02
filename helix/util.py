#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Window:
    def __init__(self, minimum, maximum, size):
        self.minimum = minimum
        self.maximum = maximum
        self.size = size

    def slide(self):
        self.size = self.size - 1 if self.size > self.minimum else self.maximum


def magic_square_params(diagonal_size):
    """
    This is a helper function to create the gene_set, optimal_fitness and
    the expected sum of all the rows, columns and diagonals.
    
    :param diagonal_size: The diagonal length of the magic square.
    :type diagonal_size: int
    """
    numbers = list(range(1, diagonal_size**2+1))
    optimal_fitness = 2 + 2 * diagonal_size
    expected_sum = diagonal_size * (diagonal_size**2 + 1) / 2
    return numbers, optimal_fitness, expected_sum
