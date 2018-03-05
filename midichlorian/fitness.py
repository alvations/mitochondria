#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Fitness:
    def __init__(self, criterion, *args, **kwargs):
        """
        Simplest single criterion fitness object.

        :param criterion: Generic container to store the fitness criterion;.
        :type criterion: object
        """
        self.criterion = criterion

    def __gt__(self, other):
        return self.criterion > other.criterion

    def __le__(self, other):
        return not self.__gt__(other)

    def __lt__(self, other):
        return not (self.__gt__(other) and self == other)

    def __ge__(self, other):
        return self.__gt__(other) or self == other

    def __str__(self):
        return "{}".format(self.criterion)


class MinimizeFitness(Fitness):
    def __init__(self, criterion):
        """
        Single criterion fitness object.
        Instead of maximizing the criterion, we minimize it.

        :param criterion: Generic container to store the fitness criterion;.
        :type criterion: object
        """
        super(MinimizeFitness, self).__init__(criterion)

    def __gt__(self, other):
        return self.criterion < other.criterion


class GapsFitness(Fitness):
    def __init__(self, criterion, gaps):
        """
        Dual criterion fitness object.
        The first maximization *criterion* will be compared first and if the
        criteron is the same, the 2nd *gap* is an inverse criterion that
        requires minimization.

        :param criterion: Generic container to store the fitness criterion.
        :type criterion: object
        """
        super(GapsFitness, self).__init__(criterion)
        self.gaps = gaps

    def __gt__(self, other):
        if self.criterion != other.criterion:
            return self.criterion > other.criterion
        return self.gaps < other.gaps

    def __str__(self):
        return "{}\t{}".format(self.criterion, self.gaps)
