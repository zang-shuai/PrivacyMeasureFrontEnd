import numpy as np
import math
import random

from pure_ldp.core import FreqOracleClient


class UEClient(FreqOracleClient):
    def __init__(self, epsilon, d, use_oue=False, index_mapper=None):
        super().__init__(epsilon, d, index_mapper=index_mapper)
        self.use_oue = use_oue
        self.update_params(epsilon, d, index_mapper)

    def update_params(self, epsilon=None, d=None, index_mapper=None):
        super().update_params(epsilon, d, index_mapper)

        if epsilon is not None:  # If epsilon changes, update probs
            const = math.pow(math.e, self.epsilon / 2)
            self.p = const / (const + 1)
            self.q = 1 - self.p

            if self.use_oue is True:
                self.p = 0.5
                self.q = 1 / (math.pow(math.e, self.epsilon) + 1)

    def _perturb(self, index):
        oh_vec = np.random.choice([1, 0], size=self.d, p=[self.q, 1 - self.q])  # If entry is 0, flip with prob q
        if random.random() < self.p:
            oh_vec[index] = 1
        return oh_vec

    def privatise(self, data):
        index = self.index_mapper(data)

        return self._perturb(index)


def getEncode(self, data):
    index = self.client.index_mapper(data)
    en = np.zeros(self.d, dtype=int)
    en[index] = 1
    return en


if __name__ == '__main__':
    import sys

    inputs = None
    with open(sys.argv[3], "r") as file:
        inputs = eval(file.read())
    epsilon = float(sys.argv[1])
    domain = eval(sys.argv[2])
    client = UEClient(epsilon, len(domain), False, lambda x: domain.index(x))
    encode_list = []
    for x in inputs:
        index = client.index_mapper(x)
        en = np.zeros(len(domain), dtype=int)
        en[index] = 1
        encode_list.append(list(en))
    data = {
        "encode_list": encode_list,
        "perturb_list": [list(client.privatise(x)) for x in inputs]
    }
    print(data)
