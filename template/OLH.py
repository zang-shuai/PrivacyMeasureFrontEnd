import numpy as np
import math
import xxhash
from sys import maxsize
import random
from pure_ldp.core import FreqOracleClient


class LHClient(FreqOracleClient):
    def __init__(self, epsilon, d, g, use_olh=False, index_mapper=None):
        super().__init__(epsilon, d, index_mapper=index_mapper)
        self.use_olh = use_olh
        self.g = g
        self.update_params(epsilon=epsilon, d=d, use_olh=True, g=g, index_mapper=index_mapper)

    def update_params(self, epsilon=None, d=None, use_olh=None, g=None, index_mapper=None):
        super().update_params(epsilon, d, index_mapper)  # Updates core params
        self.use_olh = use_olh if use_olh is not None else self.use_olh
        self.g = g if g is not None else self.g
        if self.use_olh is True:
            self.g = int(round(math.exp(self.epsilon))) + 1
        if self.epsilon is not None or self.g is not None:
            self.p = math.exp(self.epsilon) / (math.exp(self.epsilon) + self.g - 1)
            self.q = 1.0 / (math.exp(self.epsilon) + self.g - 1)

    def _perturb(self, data, seed):
        index = self.index_mapper(data)
        x = (xxhash.xxh32(str(index), seed=seed).intdigest() % self.g)
        y = x
        p_sample = np.random.random_sample()
        if p_sample > self.p - self.q:
            y = np.random.randint(0, self.g)
        return x, y

    def privatise(self, data):
        seed = random.randint(0, maxsize)  # This is sys.maxsize
        return self._perturb(data, seed)


if __name__ == '__main__':
    import sys

    inputs = None
    with open(sys.argv[3], "r") as file:
        inputs = eval(file.read())
    epsilon = float(sys.argv[1])
    domain = eval(sys.argv[2])
    # g = eval(sys.argv[4])
    client = LHClient(epsilon, len(domain), None, True, lambda x: domain.index(x))
    encode_list = []
    perturb_list = []
    for x in inputs:
        index = client.privatise(x)
        encode_list.append(index[0])
        perturb_list.append(index[1])
    data = {
        "encode_list": encode_list,
        "perturb_list": perturb_list
    }
    print(data)
