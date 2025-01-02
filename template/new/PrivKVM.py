# -*- coding: utf-8 -*-
import numpy as np
import random

class PrivKVM(object):
    def __init__(self, data: list, N_key: int, N_iter: int, epsilon: float):
        super(PrivKVM, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 总体数据
        self.data = data
        # 用户数量
        self.N_User = len(self.data)
        # 键域长度
        self.N_key = N_key
        # 迭代次数
        self.N_iter = N_iter
        # for key perturbation(1st round)
        self.p1 = np.exp(epsilon / 2) / (np.exp(epsilon / 2) + 1)
        # for value perturbation(all rounds)
        self.p2 = np.exp(epsilon / (2 * N_iter)) / (np.exp(epsilon / (2 * N_iter)) + 1)
        # 扰动数据
        self.index = []
        self.perturb = []

    def run(self):
        freqandmean = np.zeros((self.N_key, 2))
        for i in range(self.N_key):
            freqandmean[i][1] = random.uniform(-1, 1)
        self.index, self.perturb, counter = self.Perturb(freqandmean[:, 1])
        freqandmean = self.Calibrate(counter, freqandmean[:, 1])

        self.p1 = 0.5
        if self.N_iter > 1:
            for i in range(self.N_iter - 1):
                index, perturb, counter = self.Perturb(freqandmean[:, 1])
                freqandmean[:, 1] = self.Calibrate(counter, freqandmean[:, 1])[:, 1]
        return self.index, self.perturb

    def is_multi_dimensional(self, arr):
        return any(isinstance(sub_arr, list) and self.is_multi_dimensional(sub_arr) for sub_arr in arr)

    def Perturb(self, Mean):
        N_user = len(self.data)
        counter = np.zeros((3, self.N_key))
        perturb = []
        randIndex = []
        for i in range(N_user):
            randIndex.append(np.random.randint(1, self.N_key+1))
        randBit = np.random.choice([0, 1], N_user, p=[self.p1, 1 - self.p1])
        randSign = np.random.choice([-1, 1], N_user, p=[1 - self.p2, self.p2])
        for i in range(N_user):
            S = self.data[i]
            if self.is_multi_dimensional(S) == True:
                index = randIndex[i]
                flag = 0
                for j in range(len(S)):
                    # key exist
                    it = int(S[j][0])
                    if it == index:
                        key = np.random.choice([0, 1], 1, p=[1 - self.p1, self.p1])
                        value = np.random.choice([-1, 1], 1, p=[(1 - S[j][1]) / 2, (1 + S[j][1]) / 2])
                        flag = 1
                        break
                    # key does not exist
                if flag == 0:
                    m = Mean[index-1]
                    key = randBit[i]
                    value = np.random.choice([-1, 1], 1, p=[(1 - m) / 2, (1 + m) / 2])
                # perturb the value
                value = key * value * randSign[i]
            else:
                key = S[0]
                value = S[0]
                index = randIndex[i]
                # perturb the key and discrete the value
                if index == key:
                    # key exists
                    key = np.random.choice([0, 1], 1, p=[1 - self.p1, self.p1])
                    value = np.random.choice([-1, 1], 1, p=[(1 - value) / 2, (1 + value) / 2])
                else:
                    # key does not exist
                    m = Mean[index-1]
                    key = randBit[i]
                    value = np.random.choice([-1, 1], 1, p=[(1 - m) / 2, (1 + m) / 2])
                # perturb the value
                value = key * value * randSign[i]

            if value == 1:
                counter[0][index - 1] = counter[0][index - 1] + 1
            elif value == -1:
                counter[1][index - 1] = counter[1][index - 1] + 1
            counter[2][index - 1] = counter[2][index - 1] + 1

            temp = [int(key), int(value)]
            perturb.append(temp)
        return randIndex, perturb, counter

    def Calibrate(self, counter, oldMean):
        N_user = len(self.data)
        freqandmean = np.zeros((self.N_key, 2))
        freqandmean[:, 1] = np.nan * freqandmean[:, 1]

        for i in range(self.N_key):

            n1 = counter[0][i]
            n2 = counter[1][i]
            N = n1 + n2
            if N == 0:
                freqandmean[i][0] = 0
                freqandmean[i][1] = oldMean[i]
                continue

            freqandmean[i][0] = (self.p1 - 1 + N / counter[2][i]) / (2 * self.p1 - 1)

            n1 = ((self.p2 - 1) * N + n1) / (2 * self.p2 - 1)
            n1 = self.Clip(n1, 0, N)
            n2 = ((self.p2 - 1) * N + n2) / (2 * self.p2 - 1)
            n2 = self.Clip(n2, 0, N)

            freqandmean[i][1] = self.Clip((n1 - n2) / N, -1, 1)
        return freqandmean

    def Clip(self, x, lb, ub):
        if x < lb:
            x = lb
        if x > ub:
            x = ub
        return x


if __name__ == '__main__':
    import sys

    N_key = int(sys.argv[1])
    N_iter = int(sys.argv[2])
    epsilon = float(sys.argv[3])
    inputs = None
    with open(sys.argv[4], "r") as file:
        inputs = eval(file.read())

    run_ldp = PrivKVM(inputs, N_key, N_iter, epsilon)
    index_data, perturb_data = run_ldp.run()

    data = {
        "index_list": index_data,
        "perturb_list": perturb_data
    }
    print(data)