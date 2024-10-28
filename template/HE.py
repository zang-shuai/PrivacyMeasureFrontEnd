# -*- coding: utf-8 -*-
from pure_ldp.core import FreqOracleClient
import math
import random
import numpy as np


class HEClient(FreqOracleClient):
    def __init__(self, epsilon, d, index_mapper=None):
        """

        Args:
            epsilon: float - the privacy budget
            d: integer - the size of the data domain
            index_mapper: Optional function - maps data items to indexes in the range {0, 1, ..., d-1} where d is the size of the data domain
        """
        super().__init__(epsilon, d, index_mapper=index_mapper)

    def _perturb(self, oh_vec):
        """
        Used internally to peturb data using Laplacian noise following the histogram encoding technique.

        Args:
            oh_vec: A one-hot vector, where the entry of the user's data item is set to 1 and everything else 0

        Returns: a privatised noisy vector

        """
        noise = np.random.laplace(scale=(2 / self.epsilon), size=self.d)
        noisy_vec = oh_vec + noise
        return noisy_vec

    def privatise(self, data):
        """
        Used to privatise a user's data using histogram encoding (Laplace mechanism)

        Args:
            data: User's data item

        Returns: Privatised data vector

        """
        index = self.index_mapper(data)

        oh_vec = np.zeros(self.d)
        oh_vec[index] = 1

        return list(oh_vec), list(self._perturb(oh_vec))


if __name__ == '__main__':
    import sys

    inputs = None
    with open(sys.argv[3], "r") as file:
        inputs = eval(file.read())
    epsilon = float(sys.argv[1])
    domain = eval(sys.argv[2])
    client = HEClient(epsilon, len(domain), lambda x: domain.index(x))
    encode_list = []
    perturb_list = []
    for x in inputs:
        y = client.privatise(x)
        encode_list.append(y[0])
        perturb_list.append(y[1])
    data = {
        "encode_list": encode_list,
        "perturb_list": perturb_list
    }
    print(data)
