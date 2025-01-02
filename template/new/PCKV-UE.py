# -*- coding: utf-8 -*-
import numpy as np
import random

class PCKV_UE(object):
    def __init__(self, data: list, N_key: int, l: int, a: float, b: float, p: float):
        super(PCKV_UE, self).__init__()
        # 总体数据
        self.data = data
        # 用户数量
        self.N_user = len(self.data)
        # 键域长度
        self.N_key = N_key
        # 填充长度
        self.l = l
        # 键1变1的离散概率
        self.a = a
        # 键0变0的离散概率
        self.b = b
        # 值的扰动概率
        self.p = p

    def run(self):
        sample_list, perturb_list = self.UEPerturbation()
        return sample_list, perturb_list

    def sample(self, S):
        N_S = len(S)
        eta = N_S / (max(N_S, self.l))

        if np.random.binomial(1, eta, 1) == 1:
            index = random.randint(0, N_S - 1)
            key = int(S[index][0])
            value = S[index][1]
        else:
            key = self.N_key + random.randint(1, self.l)
            value = 0
        sp = list()
        sp.append(key)
        sp.append(value)
        return sp

    def Clip(self, x, lb, ub):
        if x < lb:
            x = lb
        if x > ub:
            x = ub
        return x

    def UEPerturbation(self):
        counter = np.zeros((2, self.N_key + self.l))

        sample_list = []
        perturb_list = []

        for i in range(self.N_user):
            S = self.data[i]
            sa = self.sample(S)
            key = int(sa[0])
            value = sa[1]
            x = int(np.random.choice([-1, 1], 1, p=[(1 - value) / 2, (1 + value) / 2]))
            y = np.random.choice([-1, 1, 0], self.N_key + self.l, p=[self.b / 2, self.b / 2, 1 - self.b])
            y[key - 1] = np.random.choice([x, -x, 0], 1, p=[self.a * self.p, self.a * (1 - self.p), 1 - self.a])
            counter[0] = counter[0] + np.ceil(0.5 * y)
            counter[1] = counter[1] + np.ceil(-0.5 * y)

            sample_list.append([key, x])
            perturb_list.append(y.tolist())
        return sample_list, perturb_list

if __name__ == '__main__':
    import sys

    N_key = int(sys.argv[1])
    l = int(sys.argv[2])
    a = float(sys.argv[3])
    b = float(sys.argv[4])
    p = float(sys.argv[5])
    inputs = None
    with open(sys.argv[6], "r") as file:
        inputs = eval(file.read())

    run_ldp = PCKV_UE(inputs, N_key, l, a, b, p)
    sample_data, perturb_data = run_ldp.run()

    data = {
        "sample_list": sample_data,
        "perturb_list": perturb_data
    }
    print(data)