# -*- coding: utf-8 -*-
import random
from scipy.special import comb
import math
import numpy as np

class PrivSet(object):
    def __init__(self, d: int, m: int, epsilon: float, k: int, data: list, domain: list):
        super(PrivSet, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 定义最大项数
        self.m = m
        # 定义输出子集大小
        self.k = k
        # 总体数据
        self.data = data
        # 总用户数
        self.n = len(data)
        # 定义域
        self.domain = domain
        # 定义域大小
        self.d = d
        # 填充数据
        self.pad_data = [i for i in range(d+1, d+m+1)]
        # 填充后定义域
        self.pad_domain = np.union1d(self.domain, self.pad_data)
        # 编码后的数据
        self.encode_data = []
        # 隐私处理后的数据
        self.per_data = []
        # 概率标准化
        self.omega = 0
        # 真实概率
        self.TPR = 0
        # 虚假概率
        self.FPR = 0

    def run(self):
        # 确定参数
        self.select_params()
        # 运行(d,m,e,k)-PrivSet机制
        for i in range(self.n):
            v = self.preprocess(self.data[i])
            self.encode_data.append(v)
            t = self.perturb(v)
            self.per_data.append(t)
        return self.encode_data, self.per_data

    def select_params(self):
        self.omega = comb(self.d, self.k) + math.exp(self.epsilon) * (comb(self.d + self.m, self.k) - comb(self.d, self.k))
        self.TPR = math.exp(self.epsilon) * comb(self.d + self.m - 1, self.k - 1) / self.omega
        FPR = comb(self.d - 1, self.k - 1) / self.omega
        z = self.k * (comb(self.d + self.m, self.k) - comb(self.d, self.k)) - self.m * comb(self.d + self.m - 1, self.k - 1)
        self.FPR = FPR + math.exp(self.epsilon) * (z / self.d / self.omega)

    def preprocess(self, s: list) -> list:
        x = []
        if len(s) > self.m:
            x = random.sample(s, self.m)
        else:
            x = s
            for i in range(0, self.m-len(s)):
                x = x + [self.pad_data[i]]
        return x

    def perturb(self, v: list) -> list:
        r = random.uniform(0.0, 1.0)
        # print("r=", r)
        inters = 0
        prob = comb(self.d, self.k) / self.omega
        while prob < r:
            inters = inters + 1
            prob = prob + math.exp(self.epsilon)*comb(self.m, inters)*comb(self.d, self.k-inters)/self.omega
            # if inters < 5:
            #     print("i=", inters)
            #     print(math.exp(self.epsilon))
            #     print(comb(self.m, inters))
            #     print(comb(self.d, self.k-inters)/self.omega)
            #     print("prob=", prob)
        x = np.setdiff1d(self.pad_domain, v)
        x = x.tolist()
        a = random.sample(v, inters)
        b = random.sample(x, self.k - inters)
        if len(a) == 0:
            t = b
        elif len(b) == 0:
            t = a
        else:
            t = np.union1d(a, b)
            t = t.tolist()
        return t

if __name__ == '__main__':
    import sys

    d = int(sys.argv[1])
    set_size = int(sys.argv[2])
    epsilon = float(sys.argv[3])
    k = int(sys.argv[4])
    domain = eval(sys.argv[5])
    inputs = None
    with open(sys.argv[6], "r") as file:
        inputs = eval(file.read())
    run_ldp = PrivSet(d, set_size, epsilon, k, inputs, domain)
    encode_data, perturb_data = run_ldp.run()

    data = {
        "encode_list": encode_data,
        "perturb_list": perturb_data
    }
    print(data)