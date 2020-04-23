import operator
from functools import reduce

__all__ = ['transpose', 'union', 'replace']

def transpose(matrix):
    return list(map(list, zip(*matrix)))

def replace(matrix, src, dst):
    return [[cell if cell != src else dst for cell in row] for row in matrix]

def union(*lists):
    return set(reduce(operator.add, lists))