import operator
from functools import reduce

__all__ = ['transpose', 'union']

def transpose(matrix):
    return list(map(list, zip(*matrix)))

def union(*lists):
    return set(reduce(operator.add, lists))