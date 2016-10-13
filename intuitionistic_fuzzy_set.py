#import numpy as np
import copy
import random
from ifs_lattice import *
from universal_set import *


STD_ZERO = (0, 1)
STD_ONE = (1, 0)

PI_ZERO = (0, 0)


class IFS(object):

    def __init__(self, universe, rang=None):

        self._universe = universe
        self._range = rang
        self._selector = {}

    @classmethod
    def from_IFS(cls, other):
        result = cls(other._universe, other._range)
        result._selector = copy.deepcopy(other._selector)
        return result

    @classmethod
    def random(cls, universe, rang):
        random.seed(a=1, version=2)
        result = cls(universe, rang)
        range_ = range(rang)
        result._selector = {}

        for idx in result._universe.indices():
            sample = random.sample(range_, 2)
            result._selector[idx] = (min(sample), rang - max(sample))

        return result

    def __getitem__(self, key):

        if key not in self._universe.indices():
            raise KeyError("%i is not a valide index" % key)
        else:
            return self._selector.get(key, STD_ZERO)

    def __setitem__(self, key, value):

        if key in self._universe.indices():
            self._selector[key] = value
        else:
            raise KeyError("%i is not a valide index" % key)

    def get(self, idx, default=None):
        return self._selector.get(idx, default)

    def get_range(self):
        return self._range

    def get_universe(self):
        return self._universe

    def indices(self):
        return self._universe.indices()

    def support_indices(self):
        supp_idxes = [i for i, v in self._selector.items()
                                        if v != STD_ZERO
                     ]

        return set(supp_idxes)

    def elements_split(self):
        """
        Split and return the indices, mus and nus
        in the corresponding order.
        """
        items = sorted(list(self._selector.items()), key=lambda a: a[0])
        items = list(zip(*items))
        indices = items[0]
        values = list(zip(*items[1]))
        mus, nus = values[0], values[1]
        pis = tuple([self._range - m - n for m,n in items[1]])
        return indices, mus, nus, pis

    def length(self):
        return self._universe.length()

#    def update(self, universe):
#        self._universe = universe

#    def intersection(self, rhs):
 #       result = IndicesSet(self.universe)
 #       result._item = self._item & rhs._item
 #       return result

 #   def union(self, rhs):
  #      result = IndicesSet(self.universe)
 #       result._item = self._item | rhs._item
 #       return result
