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
    # import sys
    # inputs = None
    # with open(sys.argv[3], "r") as file:
    #     inputs = eval(file.read())
    # epsilon = float(sys.argv[1])
    # domain = eval(sys.argv[2])
    # client = HEClient(epsilon, len(domain), lambda x: domain.index(x))
    # encode_list = []
    # perturb_list = []
    # for x in inputs:
    #     y = client.privatise(x)
    #     encode_list.append(y[0])
    #     perturb_list.append(y[1])
    # data = {
    #     "encode_list": encode_list,
    #     "perturb_list": perturb_list
    # }
    # print(data)

# duchi = Duchi(2.3, [10, 100])
# datas = 10 + (100 - 10) * np.random.random(10000)
# print(datas)
# privatise = duchi.privatise([50 for i in range(100)])
# print(privatise)
# print(datas)
# ans = []
# for i in range(100):
#     ans.append(duchi.get_expectation(datas))
# cdf(ans)


# datas = np.random.uniform(10, 100, 10000)
# print(datas)
# ans = []
# for i in range(100):
#     ans.append(pm.get_expectation(datas))
# cdf(ans)
# import sys
# n = int(10001)
# n_once = int(math.sqrt(n))
# n_input = n // n_once
# values = np.linspace(float(10), float(100), n_once, endpoint=True)
# print(len(list(values)))
# duchi = Duchi(float(0.3), [float(10), float(100)])
# privatise = []
# for v in values:
#     privatise.extend(duchi.privatise([v for _ in range(n_input)]))
# print(len(privatise))
