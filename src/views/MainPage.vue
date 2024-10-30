<template>
  <main>
    <Sidebar @select-form="selectForm"/>
    <MainContent v-model:formData="formData" v-model:currentForm="currentForm" @showContent="showContent"/>
  </main>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue';
import Sidebar from '../components/SideBar.vue';
import MainContent from '../components/MainContent.vue';

// 目前展示的表单类型，具体内容在formElements中
const currentForm = ref('ob_measureDiv');

// 所有的表单选项
const formData = reactive({
  input_type: {content: '', show: true},
  output_type: {content: '', show: true},
  alg_name: {content: '', show: true},
  alg_type: {content: '', show: true},
  call_method: {content: '', show: true},
  discrete_domain: {content: '', show: true},
  continue_min_domain: {content: '', show: true},
  continue_max_domain: {content: '', show: true},
  set_size_domain: {content: '', show: true},
  set_domain: {content: '', show: true},
  key_domain: {content: '', show: true},
  value_domain: {content: '', show: true},
  code_file: {content: '', show: true},
  exe_file: {content: null, show: true},
  api_file: {content: '', show: true},
  epsilon: {content: '', show: true},
  accuracy: {content: '', show: true},
  once_n: {content: '', show: true},
  whole_n: {content: '', show: true},
  ob_format: {content: '', show: true},
  duchi_format: {content: '', show: true},
  pm_format: {content: '', show: true},
  laplace_format: {content: '', show: true},
  rr_format: {content: '', show: true},
  sue_format: {content: '', show: true},
  oue_format: {content: '', show: true},
  blh_format: {content: '', show: true},
  olh_format: {content: '', show: true},
  he_format: {content: '', show: true},
  ksubset_format: {content: '', show: true},
  privKVM_format: {content: '', show: true},
  pckvUE_format: {content: '', show: true},
  pckvGRR_format: {content: '', show: true},
  dPAPPOR_format: {content: '', show: true},
  OLHSampling_format: {content: '', show: true},
  OUESampling_format: {content: '', show: true},
  privSet_format: {content: '', show: true},
  wheel_format: {content: '', show: true},
  ldpMinner_format: {content: '', show: true},

});

// 某个具体的算法能够展示的表单项配置：
const formDataOfAlg = {
  '黑盒': [
    "alg_name", "alg_type", "input_type", "output_type", "call_method",
    "code_file", "ob_format", "epsilon", "once_n"
  ],
  ob_measure: [
    "alg_name", "alg_type", "input_type", "output_type", "call_method",
    "code_file", "ob_format", "epsilon", "once_n"
  ],
  Duchi: [
    "alg_name", "alg_type", "call_method", "code_file", "continue_min_domain", "continue_max_domain",
    "duchi_format", "epsilon", "whole_n"
  ],
  PM: [
    "alg_name", "alg_type", "call_method", "code_file", "continue_min_domain", "continue_max_domain",
    "pm_format", "epsilon", "whole_n"
  ],
  Laplace: [
    "alg_name", "alg_type", "call_method", "code_file", "continue_min_domain", "continue_max_domain",
    "laplace_format", "epsilon", "whole_n"
  ],
  RR: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "rr_format", "epsilon", "whole_n"
  ],
  SUE: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "sue_format", "epsilon", "whole_n"
  ],
  OUE: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "oue_format", "epsilon", "whole_n"
  ],
  BLH: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "blh_format", "epsilon", "whole_n"
  ],
  OLH: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "olh_format", "epsilon", "whole_n"
  ],
  HE: [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "he_format", "epsilon", "whole_n"
  ],
  'k-Subset': [
    "call_method", "alg_name", "alg_type", "discrete_domain", "code_file", "ksubset_format", "epsilon", "whole_n"
  ],
  PrivKVM: [
    "alg_name", "call_method", "alg_type", "key_domain", "value_domain", "code_file",
    "privKVM_format", "epsilon", "whole_n"
  ],
  'PCKV-UE': [
    "alg_name", "call_method", "alg_type",  "key_domain", "value_domain", "code_file",
    "pckvUE_format", "epsilon", "whole_n"
  ],
  'PCKV-GRR': [
    "alg_name", "call_method", "alg_type",  "key_domain", "value_domain", "code_file",
    "pckvGRR_format", "epsilon", "whole_n"
  ],
  'd-PAPPOR': [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "dPAPPOR_format", "epsilon", "whole_n"
  ],
  OLHSampling: [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "OLHSampling_format", "epsilon", "whole_n"
  ],
  OUESampling: [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "OUESampling_format", "epsilon", "whole_n"
  ],
  PrivSet: [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "privSet_format", "epsilon", "whole_n"
  ],
  Wheel: [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "wheel_format", "epsilon", "whole_n"
  ],
  LdpMinner: [
    "alg_name", "call_method", "alg_type",
    "set_size_domain", "set_domain", "code_file", "ldpMinner_format", "epsilon", "whole_n"
  ],
}

const select2Properity = {
  code_: ["code_file"],
  exe_: ["exe_file"],
  // api_: ["api_file", "api_encode"],
};

// const formElements = {
//   ob_measureDiv: {
//     input: new Set([
//       "alg_name", "alg_type", "input_type", "output_type", "call_method",
//       "code_file", "code_whole", "epsilon", "once_n"
//     ]),
//     select: "code_",
//     code_: ["code_file", "code_whole"],
//     exe_: ["exe_file", "exe_whole"],
//     api_: ["api_file", "api_whole"],
//   },
//   ab_discreteDiv: {
//     input: new Set([
//       "alg_name", "alg_type", "discrete_domain", "call_method", "code_file",
//       "code_encode", "epsilon", "whole_n"
//     ]),
//     select: "code_",
//     code_: ["code_file", "code_encode"],
//     exe_: ["exe_file", "exe_encode"],
//     api_: ["api_file", "api_encode"],
//   },
//   ab_numericalDiv: {
//     input: new Set([
//       "call_method", "alg_name", "alg_type", "continue_min_domain",
//       "continue_max_domain", "code_file", "code_encode", "epsilon", "whole_n"
//     ]),
//     select: "code_",
//     code_: ["code_file", "code_encode"],
//     exe_: ["exe_file", "exe_encode"],
//     api_: ["api_file", "api_encode"],
//   },
//   ab_setDiv: {
//     input: new Set([
//       "alg_name", "call_method", "alg_type",
//       "set_size_domain", "set_domain", "code_file", "epsilon", "whole_n"
//     ]),
//     select: "code_",
//     code_: ["code_file", "code_encode"],
//     exe_: ["exe_file", "exe_encode"],
//     api_: ["api_file", "api_encode"],
//   },
//   ab_key_valueDiv: {
//     input: new Set([
//       "alg_name", "call_method", "alg_type", "kv_domain", "code_file",
//       "code_encode", "epsilon", "whole_n"
//     ]),
//     select: "code_",
//     code_: ["code_file", "code_encode"],
//     exe_: ["exe_file", "exe_encode"],
//     api_: ["api_file", "api_encode"],
//   },
// };

const selectForm = (selectDiv, alg) => {
  // 获取某个具体算法能够展示的表单项
  let formDataOfAlgList = formDataOfAlg[alg];
  console.log("formDataOfAlgList", formDataOfAlgList, alg);
  // 遍历 formData 的键，处理显示与隐藏
  Object.keys(formData).forEach((formDataKey) => {
    if (formDataOfAlgList.includes(formDataKey)) {
      formData[formDataKey].show = true; // 显示相关输入项
    } else {
      formData[formDataKey].show = false; // 隐藏不相关输入项
      formData[formDataKey].content = 0;  // 填充隐藏项默认值 0
    }
  });

  formData.alg_name.content = alg;
  formData.alg_type.content = selectDiv;

  formData.call_method.content = 'code_input';
  currentForm.value = selectDiv;

  setDefaultValue(selectDiv, alg);
};

const showContent = (select) => {
  console.log("debug22 ", select)
  console.log("debug2233", formData);
  for (let oldSelect of ["code_file", "exe_file", "api_file"]) {
    console.log("debug3333", oldSelect, formData, formData[oldSelect]);
    formData[oldSelect].show = false;
  }

  for (let properity of select2Properity[select]) {
    formData[properity].show = true
  }

  formData.call_method.content = select + 'input';
};

const setDefaultValue = async (selectDiv, alg) => {
  const response = await fetch('/template/' + alg + '.py');
  if (!response.ok) {
    throw new Error('读取 TXT 文件失败');
  }
  // 设置选择某个算法之后的默认初始值
  if (selectDiv === "ab_discreteDiv" && alg === "RR") {
    formData.discrete_domain.content = "[i for i in range(1, 11)]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "OUE") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "SUE") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "HE") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "KSubset") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "BLH") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_discreteDiv" && alg === "OLH") {
    formData.discrete_domain.content = "[1,2,3,4,5,6,7,8,9]"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_numericalDiv" && alg === "Duchi") {
    formData.continue_min_domain.content = '1'
    formData.continue_max_domain.content = '9'
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_numericalDiv" && alg === "PM") {
    formData.continue_min_domain.content = '1'
    formData.continue_max_domain.content = '9'
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_numericalDiv" && alg === "Laplace") {
    formData.continue_min_domain.content = '1'
    formData.continue_max_domain.content = '9'
    formData.code_file.content = await response.text()
    formData.epsilon.content = 0.4
    formData.whole_n.content = 10000
  } else if (alg === "PrivKVM") {
    formData.key_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = `# -*- coding: utf-8 -*-
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
    print(data)`;
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (alg === "PCKV-UE") {
    formData.key_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = `# -*- coding: utf-8 -*-
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
    print(data)`;
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  }  else if (alg === "PCKV-GRR") {
    formData.key_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = `# -*- coding: utf-8 -*-
import numpy as np
import random

class PCKV_GRR(object):
    def __init__(self, data: list, N_key: int, l: int, a: float, b: float, p: float):
        super(PCKV_GRR, self).__init__()
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
        sample_list, perturb_list = self.Perturbation()
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

    def Perturbation(self):
        counter = np.zeros((2, self.N_key + self.l))
        randValue = np.random.choice([-1, 1], self.N_user, p=[0.5, 0.5])

        sample_list = []
        perturb_list = []

        for i in range(self.N_user):
            S = self.data[i]
            sa = self.sample(S)
            key = (int)(sa[0])
            value = sa[1]
            x = np.random.choice([-1, 1], 1, p=[(1 - value) / 2, (1 + value) / 2])

            sample_list.append([int(key), int(x)])

            flag = int(np.random.choice([-1, 1], 1, p=[1 - self.a, self.a]))
            if flag == 1:
                value = x * np.random.choice([1, -1], 1, p=[self.p, 1 - self.p])
            else:
                temp = random.randint(1, self.N_key + self.l - 1)
                if temp >= key:
                    key = temp + 1
                else:
                    key = temp
                value = randValue[i]

            counter[0][key - 1] = counter[0][key - 1] + (value == 1)
            counter[1][key - 1] = counter[1][key - 1] + (value == -1)

            perturb_list.append([int(key), int(value)])

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

    run_ldp = PCKV_GRR(inputs, N_key, l, a, b, p)
    sample_data, perturb_data = run_ldp.run()

    data = {
        "sample_list": sample_data,
        "perturb_list": perturb_data
    }
    print(data)`;
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_setDiv" && alg === "PrivSet") {
    formData.set_size_domain.content = 4
    formData.set_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = `# -*- coding: utf-8 -*-
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
    print(data)`;
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (alg === 'Wheel') {
    formData.set_size_domain.content = 4
    formData.set_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = `# -*- coding: utf-8 -*-
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
`
    formData.epsilon.content = 2
    formData.whole_n.content = 10000
  }
}

onMounted(() => {
  selectForm('ob_measureDiv', 'ob_measure');
  formData.call_method.content = 'code_input';
  formData.input_type.content = 'single_discrete_input';
});
</script>

<style scoped>
main {
  display: flex;
  flex-wrap: nowrap;
  height: 100vh;
  max-height: 100vh;
  overflow-x: auto;
  overflow-y: hidden;
}

.b-example-divider {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.1);
  border: solid rgba(0, 0, 0, 0.15);
  border-width: 1px 0;
  box-shadow: inset 0 0.5em 1.5em rgba(0, 0, 0, 0.1),
  inset 0 0.125em 0.5em rgba(0, 0, 0, 0.15);
}

.scrollable {
  overflow-y: auto;
  max-height: 100vh;
}
</style>