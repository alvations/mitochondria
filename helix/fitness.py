#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Fitness:
    def __init__(self, criterion, *args, **kwargs):
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
        super(MinimizeFitness, self).__init__(criterion)

    def __gt__(self, other):
        return self.criterion < other.criterion


class GapsFitness(Fitness):
    def __init__(self, criterion, gaps):
        super(GapsFitness, self).__init__(criterion)
        self.gaps = gaps

    def __gt__(self, other):
        if self.criterion != other.criterion:
            return self.criterion > other.criterion
        return self.gaps < other.gaps

    def __str__(self):
        return "{}\t{}".format(self.criterion, self.gaps)
