# -*- coding: utf-8 -*-
import time
import math
import numpy as np
import xxhash
from collections import Counter

class Wheel(object):
    def __init__(self, epsilon: float, p: float, data: list, m: int):
        super(Wheel, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 定义域
        self.domain = []
        # 定义域的长度
        self.d = 0
        # 总体数据
        self.data = data
        # 每个用户的数据条数
        self.m = m
        # 定义覆盖范围参数
        self.p = p
        # 哈希种子
        self.s_data = []
        # 哈希后数据
        self.v_data = []
        # 扰动后数据
        self.z_data = []
        # 总用户数量
        self.n = len(data)

    def run(self):
        for i in range(self.n):
            v = self.encode(self.data[i], i)
            self.s_data.append(i)
            self.v_data.append(v)
            res = self.merge(v)
            left = res[0]
            right = res[1]
            z = self.perturb(left, right)
            self.z_data.append(z)
        # print("epsilon:", self.epsilon)
        # print("m:", self.m)
        # print("p:", self.p)
        # print("v_data:", self.v_data)
        # print("z_data:", self.z_data)
        return self.v_data, self.z_data

    # x此时传入的是用户的原始数据，并不是该数据在domain中的位置
    # pos为用户原始数据在原始数据集合中的位置，也是哈希函数的种子
    def encode(self, x: list, pos: int) -> list:
        # x被哈希到0.0到1.0中的一个数字
        v = []
        for i in range(self.m):
            rs = xxhash.xxh32(str(x[i]), seed=pos).intdigest() % 10000000000
            v.append(rs/10000000000)
        return v

    def merge(self, v: list) -> list:
        b = math.ceil(1/self.p)
        left = []
        right = []
        # left,right的下标从1开始,left[1],right[1]
        left.append(0)
        right.append(0)
        # 初始化桶边界
        for i in range(b):
            left.append(min(i*self.p, 1.0))
            right.append((i-1)*self.p)
        # 根据v更改桶边界
        for i in range(len(v)):
            # 判断v[i]在第几个桶
            j = math.ceil(v[i]/self.p)
            left[j] = min(v[i], left[j])
            if j < b:
                right[j+1] = max(v[i]+self.p, right[j+1])
            else:
                right[1] = max(v[i]+self.p-1, right[1])
        # 合并桶边界
        left[b] = max(left[b], right[b])
        right[b] = right[1] + 1
        for k in range(1, b):
            left[k] = max(left[k], right[k])
            right[k] = right[k+1]
        return [left, right]

    # 将集合扰动成一个在[0,1)的值z
    def perturb(self, left: list, right: list) -> float:
        b = math.ceil(1 / self.p)
        l = np.sum(np.subtract(right, left))
        r = np.random.uniform(0.0, 1.0)
        a = 0.0
        omega = self.m*self.p*math.exp(self.epsilon) + (1-self.m*self.p)
        for k in range(1, b+1):
            a = a + math.exp(self.epsilon)*(right[k] - left[k])/omega
            if a > r:
                z = right[k] - (a - r)*omega/math.exp(self.epsilon)
                break
            a = a + (omega - l*math.exp(self.epsilon)) * (left[k % b+1]+math.floor(k*self.p)-right[k]) / ((1-l)*omega)
            if a > r:
                z = left[k % b+1] - (a - r) * (1 - l) * omega / (omega - l*math.exp(self.epsilon))
                break
        z = z % 1.0
        return z

if __name__ == '__main__':
    import sys

    epsilon = float(sys.argv[1])
    p = float(sys.argv[2])
    set_size = int(sys.argv[3])
    inputs = None
    with open(sys.argv[4], "r") as file:
        inputs = eval(file.read())
    run_ldp = Wheel(epsilon, p, inputs, set_size)
    encode_data, perturb_data = run_ldp.run()

    data = {
        "encode_list": encode_data,
        "perturb_list": perturb_data
    }
    print(data)