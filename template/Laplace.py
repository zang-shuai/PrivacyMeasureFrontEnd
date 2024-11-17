import numpy as np
import random


class LaplaceMechanism(object):
    def __init__(self, epsilon, domain):
        self.epsilon = epsilon
        self.domain = domain
        self.a = domain[0]
        self.b = domain[1]

    def normalization_data(self, datas):
        # 将数据归一化到 [0, 1]
        return [(data - self.a) / (self.b - self.a) for data in datas]

    def privatise(self, datas):
        datas = self.normalization_data(datas)
        sensitivity = 1.0  # 因为数据已经归一化
        scale = sensitivity / self.epsilon
        privatized_data = [data + np.random.laplace(0, scale) for data in datas]
        return privatized_data

    def get_expectation(self, datas):
        privatized_data = self.privatise(datas)
        # 对归一化后的数据计算均值，并反归一化
        estimated_mean = np.mean(privatized_data) * (self.b - self.a) + self.a
        return estimated_mean


if __name__ == '__main__':
    import sys

    epsilon = float(sys.argv[1])
    min_value = float(sys.argv[2])
    max_value = float(sys.argv[3])
    inputs = None
    with open(sys.argv[4], "r") as file:
        inputs = eval(file.read())

    lm = LaplaceMechanism(epsilon, [min_value, max_value])
    outputs = lm.privatise(inputs)
    print({
        "inputs": inputs,
        "outputs": outputs,
    })
