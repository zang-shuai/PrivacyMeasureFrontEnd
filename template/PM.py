import numpy as np
import random


class PiecewiseMechanism(object):
    def __init__(self, epsilon, domain):
        self.epsilon = epsilon
        self.domain = domain
        self.a = domain[0]
        self.b = domain[1]
        self.d = np.arange(self.a, self.b, 0.1)

    def normalization_data(self, datas):
        try:
            ans = [2 * data / (self.b - self.a) + (self.a + self.b) / (self.a - self.b) for data in datas]
        except Exception:
            ans = [2 * datas / (self.b - self.a) + (self.a + self.b) / (self.a - self.b), ]
        return ans

    def privatise(self, datas):
        C = (np.exp(self.epsilon / 2) + 1) / (np.exp(self.epsilon / 2) - 1)
        p = (np.exp(self.epsilon) - np.exp(self.epsilon / 2)) / (2 * np.exp(self.epsilon / 2) + 2)
        ans = []
        datas = self.normalization_data(datas)
        for data in datas:
            l = (C + 1) / 2 * data - (C - 1) / 2
            r = l + C - 1
            p1 = (C + l) * p / np.exp(self.epsilon)
            p2 = (r - l) * p
            p3 = (C - r) * p / np.exp(self.epsilon)
            getOne = random.choices(
                [np.random.uniform(-C, l, 1)[0], np.random.uniform(l, r, 1)[0], np.random.uniform(r, C, 1)[0]],
                weights=[p1, p2, p3], k=1)[0]
            ans.append(getOne)
        if len(ans) == 1:
            return ans[0]
        return ans

    def get_expectation(self, datas):
        return ((sum(self.privatise(datas)) / len(datas)) * (self.b - self.a) + self.a + self.b) / 2


if __name__ == '__main__':
    import sys

    epsilon = float(sys.argv[1])
    min_value = float(sys.argv[2])
    max_value = float(sys.argv[3])
    inputs = None
    with open(sys.argv[4], "r") as file:
        inputs = eval(file.read())

    pm = PiecewiseMechanism(epsilon, [min_value, max_value])
    privatise = []
    for v in inputs:
        privatise.append(pm.privatise(v))
    print({
        "inputs": list(set(inputs)),
        "outputs": privatise,
    })

#
# if __name__ == '__main__':
#     import sys
#
#     pm = PiecewiseMechanism(0.3, [10, 100])
#
# datas = np.random.uniform(0, 100, 10000)
#
# print(datas)
# ans = []
# for i in range(100):
#     ans.append(pm.get_expectation(datas))
# cdf(ans)

#
# pm = PiecewiseMechanism(0.8, [10, 100])
# datas = []
# for i in range(10, 101):
#     datas.append([i for _ in range(100000)])
#
# ans = []
# for data in datas:
#     d = pm.privatise(data)
#     # print(len(p))
#
#     # ans.append(count_probability(d))
#     C = 10
#     sequence = np.linspace(-C, C, 1000)
#     model = KernelDensity(bandwidth=0.125, kernel='gaussian')
#     model.fit(np.array(d)[:, np.newaxis])
#     f = model.score_samples(sequence[:, np.newaxis])
#     ans.append(f)
#
# print(len(ans))
# print(len(ans[0]))
#
#
#
#
# a = list(itertools.combinations(range(91), 2))
# print(a)
#
# # print(math.fabs(ans[0]-ans[-1]))
# res = []
# print(ans[0][:10])
# print(ans[-1][:10])
# for i in range(len(ans[0])):
#     res.append(math.fabs(ans[0][i]-ans[-1][i]))
#
# print(res)
#
# p = []
# for ii,j in itertools.combinations(range(91), 2):
#     res = []
#     print(len(p))
#     # print(ans[0][:10])
#     # print(ans[-1][:10])
#     for i in range(len(ans[0])):
#         res.append(math.fabs(ans[ii][i] - ans[j][i]))
#     p.append(max(res))
#     # print(res)
# print(max(p))
# # import math
# #
# # e = 1.3
# # print((math.exp(e/2)+1)/((math.exp(e/2)-1)))
