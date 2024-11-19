import math

import numpy as np
import random


def is_iterable(variable):
    try:
        iter(variable)
        return True
    except TypeError:
        return False


class Duchi(object):
    def __init__(self, epsilon, inputData):
        self.epsilon = epsilon
        self.a = inputData[0]
        self.b = inputData[1]

    def privatise(self, datas):
        x = (np.exp(self.epsilon) + 1) / (np.exp(self.epsilon) - 1)
        ans = []
        if is_iterable(datas):
            for data in datas:
                x_p = 2 * data / (self.b - self.a) + (self.a + self.b) / (self.a - self.b)
                p = x_p / (2 * x) + 1 / 2
                ans.append(random.choices([x, -x], weights=[p, 1 - p], k=1)[0])
        else:
            data = datas
            x_p = 2 * data / (self.b - self.a) + (self.a + self.b) / (self.a - self.b)
            p = x_p / (2 * x) + 1 / 2
            ans.append(random.choices([x, -x], weights=[p, 1 - p], k=1)[0])
            return ans[0]

        return ans

    def get_expectation(self, datas):
        return ((sum(self.privatise(datas)) / len(datas)) * (self.b - self.a) + self.a + self.b) / 2


if __name__ == '__main__':
    import sys

    epsilon = float(sys.argv[1])
    min_value = float(sys.argv[2])
    max_value = float(sys.argv[3])
    # inputs = eval(sys.argv[4])
    inputs = None
    with open(sys.argv[4], "r") as file:
        inputs = eval(file.read())

    duchi = Duchi(epsilon, [min_value, max_value])
    privatise = []
    for v in inputs:
        privatise.append(duchi.privatise(v))
    print({
        "inputs": list(set(inputs)),
        "outputs": privatise,
    })