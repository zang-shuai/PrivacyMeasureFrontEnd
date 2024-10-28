<template>
  <el-container class="result-container">
    <el-main>
      <el-row :gutter="20" class="mb-4">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>真实的隐私预算</h3>
            </template>
            <div class="data-info">{{ realPrivacyBudget }}</div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>评估的隐私预算</h3>
            </template>
            <div class="data-info">{{ displayedEstimatedBudget.toFixed(10) }}</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mb-4">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>数据数量</h3>
            </template>
            <div class="data-info">{{ inputs_n }}</div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>数据域大小</h3>
            </template>
            <div class="data-info">{{ input_kinds_n }}</div>
          </el-card>
        </el-col>
      </el-row>

      <el-card class="mb-4">
<!--        <template #header>-->
<!--          <div class="card-header">-->
<!--            <h2>详细数据</h2>-->
<!--            <el-button type="primary" @click="fetchDetailedData">获取详细数据</el-button>-->
<!--          </div>-->
<!--        </template>-->

        <el-collapse v-if="(inputs.length > 0 || outputs.length > 0)">
          <el-collapse-item title="Inputs" name="1">
            <el-table :data="paginatedInputs" border style="width: 100%">
              <el-table-column v-for="(col, index) in inputColumns" :prop="col" :key="index"
                :label="col"></el-table-column>
            </el-table>
            <el-pagination v-if="inputs.length > pageSize" :current-page="inputsCurrentPage" :page-size="pageSize"
              :total="inputs.length" @current-change="handleInputsPageChange" layout="prev, pager, next"
              class="mt-4"></el-pagination>
          </el-collapse-item>

          <el-collapse-item title="Outputs" name="2">
            <el-table :data="paginatedOutputs" border style="width: 100%">
              <el-table-column v-for="(col, index) in outputColumns" :prop="col" :key="index"
                :label="col"></el-table-column>
            </el-table>
            <el-pagination v-if="outputs.length > pageSize" :current-page="outputsCurrentPage" :page-size="pageSize"
              :total="outputs.length" @current-change="handleOutputsPageChange" layout="prev, pager, next"
              class="mt-4"></el-pagination>
          </el-collapse-item>
        </el-collapse>

        <el-empty v-else description="暂无详细数据"></el-empty>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { useResultStore } from '@/stores/result';
import * as echarts from "echarts"

const resultStore = useResultStore();
const inputs = computed(() => resultStore.inputs);
const outputs = computed(() => resultStore.outputs);
const inputs_n = computed(() => resultStore.inputs_n);
const input_kinds_n = computed(() => resultStore.input_kinds_n);

const formattedInputs = computed(() => {
  return inputs.value.map((input, index) => {
    if (Array.isArray(input)) {
      return {
        index: index + 1,
        ...input.reduce((acc, val, idx) => {
          acc[`value_${idx + 1}`] = val;
          return acc;
        }, {})
      };
    } else {
      return {
        index: index + 1,
        value_1: input
      };
    }
  });
});

const formattedOutputs = computed(() => {
  return outputs.value.map((output, index) => {
    if (Array.isArray(output)) {
      return {
        index: index + 1,
        ...output.reduce((acc, val, idx) => {
          acc[`value_${idx + 1}`] = val;
          return acc;
        }, {})
      };
    } else {
      return {
        index: index + 1,
        value_1: output
      };
    }
  });
});

const pageSize = 10; // 每页显示的数据条数
const inputsCurrentPage = ref(1);
const outputsCurrentPage = ref(1);

const showDetailedData = ref(false);

const inputColumns = computed(() => {
  if (inputs.value.length === 0) return ['index'];
  const firstInput = inputs.value[0];
  if (Array.isArray(firstInput)) {
    return ['index', ...firstInput.map((_, idx) => `value_${idx + 1}`)];
  } else {
    return ['index', 'value_1'];
  }
});

const outputColumns = computed(() => {
  if (outputs.value.length === 0) return ['index'];
  const firstOutput = outputs.value[0];
  if (Array.isArray(firstOutput)) {
    return ['index', ...firstOutput.map((_, idx) => `value_${idx + 1}`)];
  } else {
    return ['index', 'value_1'];
  }
});

const paginatedInputs = computed(() => {
  const start = (inputsCurrentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return formattedInputs.value.slice(start, end);
});

const paginatedOutputs = computed(() => {
  const start = (outputsCurrentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return formattedOutputs.value.slice(start, end);
});

const handleInputsPageChange = (page) => {
  inputsCurrentPage.value = page;
};

const handleOutputsPageChange = (page) => {
  outputsCurrentPage.value = page;
};

const base_url = 'http://localhost:8000/api/';

const realPrivacyBudget = computed(() => resultStore.epsilon);
const estimatedPrivacyBudget = computed(() => resultStore.result);

const displayedEstimatedBudget = ref(0);

// const fetchDetailedData = () => {
//   // 从后端获取数据
//   const data = { id: resultStore.params['id'] };
//
//   fetch(base_url + 'ldp_result', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(data)
//   })
//     .then(response => response.json())
//     .then(data => {
//       console.log('Success:', data);
//       resultStore.setInputs(data.inputs);
//       resultStore.setOutputs(data.outputs);
//       showDetailedData.value = true;
//       ElMessage.success('详细数据获取成功');
//     })
//     .catch((error) => {
//       console.error('Error:', error);
//       ElMessage.error('获取详细数据失败，请重试');
//     });
//
//   // 直接从 Pinia 存储中获取数据
//   // if (inputs.value.length > 0 || outputs.value.length > 0) {
//   //   showDetailedData.value = true;
//   //   ElMessage.success('详细数据获取成功');
//   // } else {
//   //   ElMessage.warning('暂无详细数据');
//   // }
// };

onMounted(() => {
  animateEstimatedBudget();
});

const animateEstimatedBudget = () => {
  const duration = 2000; // 动画持续时间（毫秒）
  const steps = 60; // 动画步数
  const stepDuration = duration / steps;
  const stepValue = estimatedPrivacyBudget.value / steps;

  let currentStep = 0;

  const animation = setInterval(() => {
    if (currentStep < steps) {
      displayedEstimatedBudget.value += stepValue;
      currentStep++;
    } else {
      displayedEstimatedBudget.value = estimatedPrivacyBudget.value;
      clearInterval(animation);
    }
  }, stepDuration);
};
</script>

<style scoped>
.result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

h1,
h2 {
  color: #303133;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-descriptions {
  margin-top: 20px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  margin: 0;
}

.el-collapse {
  margin-top: 20px;
}

.el-list-item {
  padding: 10px 0;
}
</style>