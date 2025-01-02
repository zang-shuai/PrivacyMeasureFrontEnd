<template>
  <main>
    <Sidebar @select-form="selectForm" @publish-mode="handlePublishMode" />

    <MainContent v-if="!isPublishMode" v-model:formData="formData" v-model:currentForm="currentForm"
      @showContent="showContent" />

    <div v-else>
      <PublishContent :alg_name="alg_name"/>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import Sidebar from '../components/SideBar.vue';
import MainContent from '../components/MainContent.vue';
import PublishContent from './PublishData.vue';

const alg_name = ref("k")

// 目前展示的表单类型，具体内容在formElements中
const currentForm = ref('ob_measureDiv');

const isPublishMode = ref(false);

const handlePublishMode = (mode) => {
  if (mode === "collection_mode") {
    isPublishMode.value = false;
  } else {
    isPublishMode.value = true;
    alg_name.value = mode;
  }
};

// 所有的表单选项
const formData = reactive({
  input_type: { content: '', show: true },
  output_type: { content: '', show: true },
  alg_name: { content: '', show: true },
  alg_type: { content: '', show: true },
  call_method: { content: '', show: true },
  discrete_domain: { content: '', show: true },
  continue_min_domain: { content: '', show: true },
  continue_max_domain: { content: '', show: true },
  set_size_domain: { content: '', show: true },
  set_domain: { content: '', show: true },
  key_domain: { content: '', show: true },
  value_domain: { content: '', show: true },
  code_file: { content: '', show: true },
  exe_file: { content: null, show: true },
  api_file: { content: '', show: true },
  epsilon: { content: '', show: true },
  accuracy: { content: '', show: true },
  once_n: { content: '', show: true },
  whole_n: { content: '', show: true },
  ob_format: { content: '', show: true },
  duchi_format: { content: '', show: true },
  pm_format: { content: '', show: true },
  laplace_format: { content: '', show: true },
  rr_format: { content: '', show: true },
  sue_format: { content: '', show: true },
  oue_format: { content: '', show: true },
  blh_format: { content: '', show: true },
  olh_format: { content: '', show: true },
  he_format: { content: '', show: true },
  ksubset_format: { content: '', show: true },
  privKVM_format: { content: '', show: true },
  pckvUE_format: { content: '', show: true },
  pckvGRR_format: { content: '', show: true },
  dPAPPOR_format: { content: '', show: true },
  OLHSampling_format: { content: '', show: true },
  OUESampling_format: { content: '', show: true },
  privSet_format: { content: '', show: true },
  wheel_format: { content: '', show: true },
  ldpMinner_format: { content: '', show: true },

});

// 某个具体的算法能够展示的表单项配置：
const formDataOfAlg = {
  '第一类：通用的数据采集算法评估': [
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
    "alg_name", "call_method", "alg_type", "key_domain", "value_domain", "code_file",
    "pckvUE_format", "epsilon", "whole_n"
  ],
  'PCKV-GRR': [
    "alg_name", "call_method", "alg_type", "key_domain", "value_domain", "code_file",
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


// 第一类：通用的数据采集算法评估
// 第二类：第二类：数值型数据采集算法评估评估数据采集算法评估
// 第三类：第三类：类别型数据采集算法评估数据采集算法评估
// 第四类：第四类：集合型数据采集算法评估数据采集算法评估
// 第五类：kv 型数据采集算法评估

// 第六类：通用的数据发布算法评估
// 第七类：k-匿名数据发布算法评估
// 第八类：l-多样性数据发布算法评估
// 第九类：t-接近性数据发布算法评估


const selectForm = (selectDiv, alg) => {
  // let code_file_show =  formData.code_file.show;
  // let exe_file_show =  formData.exe_file.show;
  // alert("xxxxx");
  // formData['output_type'].content = outputTypeOptions[0].value; // 设置为第一个选项的值
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
  // formData.code_file.show = code_file_show;
  // formData.exe_file.show = exe_file_show;
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
    formData.code_file.content = await response.text()
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (alg === "PCKV-UE") {
    formData.key_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (alg === "PCKV-GRR") {
    formData.key_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (selectDiv === "ab_setDiv" && alg === "PrivSet") {
    formData.set_size_domain.content = 4
    formData.set_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 4
    formData.whole_n.content = 10000
  } else if (alg === 'Wheel') {
    formData.set_size_domain.content = 4
    formData.set_domain.content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50"
    formData.code_file.content = await response.text()
    formData.epsilon.content = 2
    formData.whole_n.content = 10000
  } else if (selectDiv === "ob_measureDiv") {
    // formData.set_size_domain.content = 4
    formData.discrete_domain.content = "[1, 2, 3, 4, 5, 6, 7, 8, 9]"
    formData.continue_min_domain.content = 1
    formData.input_type.content = 'single_discrete_input'
    formData.output_type.content = 'single_discrete_output'
    formData.continue_max_domain.content = 100
    formData.code_file.content = await response.text()
    formData.epsilon.content = 4
    formData.once_n.content = 10000
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