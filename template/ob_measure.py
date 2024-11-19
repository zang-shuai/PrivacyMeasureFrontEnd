# -*- coding: utf-8 -*-
from pure_ldp.core import FreqOracleClient
import math
import random


class DEClient(FreqOracleClient):
    def __init__(self, epsilon, d, index_mapper=None):
        super().__init__(epsilon, d, index_mapper)
        self.update_params(epsilon, d, index_mapper)

    def update_params(self, epsilon=None, d=None, index_mapper=None):
        super().update_params(epsilon, d, index_mapper)

        if epsilon is not None or d is not None:  # If epsilon changes, update probs
            self.const = math.pow(math.e, self.epsilon) + self.d - 1
            self.p = (math.pow(math.e, self.epsilon)) / (self.const)
            self.q = 1 / self.const

    def _perturb(self, data):
        if random.random() < self.p:
            return data
        else:
            perturbed_data = random.randint(0, self.d - 2)
            if perturbed_data == data:
                return self.d - 1
            else:
                return perturbed_data

    def privatise(self, data):
        index = self.index_mapper(data)  # Maps data to the range {0,...,d-1}
        return self._perturb(index)


if __name__ == '__main__':
    import sys

    inputs = None
    with open(sys.argv[3], "r") as file:
        inputs = eval(file.read())
    epsilon = float(sys.argv[1])
    domain = eval(sys.argv[2])
    client = DEClient(epsilon, len(domain), lambda x: domain.index(x))
    print([[client.privatise(x),] for x in inputs])
