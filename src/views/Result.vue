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
              <h3>度量的隐私预算</h3>
            </template>
            <div class="data-info">{{ displayedEstimatedBudget.toFixed(10) }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mb-4">
        <el-col>
          <el-card>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div class="echarts" ref="realChartRef" style="width: 48%; height: 400px;"></div>
              <div class="echarts" ref="chartRef" style="width: 48%; height: 400px;"></div>
            </div>
            <div class="data-info">{{ result_message }}</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mb-4">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>测试数据数量</h3>
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
import { ref, onMounted, computed, onUnmounted } from 'vue';
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
    if (firstInput.length < input_kinds_n.value) {
      // 使表格显示完全
      for (let i = firstInput.length; i < input_kinds_n.value; i++) {
        firstInput.push(null); // 或者使用其他默认值
      }
    }
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
let result_message = computed(() => {
  let boo = Math.abs(realPrivacyBudget.value - estimatedPrivacyBudget.value) / realPrivacyBudget.value;
  if (boo > 0.1) {
    return "度量值与预设值差距较大，请注意检查代码bug或算法正确性，或者增加测试数据量重新测试";
  } else {
    return "度量值与预设值差距较小，测试结果可信";
  }
});

const displayedEstimatedBudget = ref(0);

const estimatedOption = ref({
  tooltip: {
    formatter: "{a} <br/>{b} : {c}%",
  },
  series: [
    {
      name: "度量隐私预算",
      type: "gauge",
      progress: {
        show: true,
      },
      detail: {
        valueAnimation: true,
        formatter: "{value}",
      },
      min: 0, // 最小刻度
      max: realPrivacyBudget.value * 2, // 最大刻度
      data: [
        {
          value: parseFloat(estimatedPrivacyBudget.value.toFixed(2)),
          name: "Epsilon",
        },
      ],
    },
  ],
});

const realOption = ref({
  tooltip: {
    formatter: "{a} <br/>{b} : {c}%",
  },
  series: [
    {
      name: "真实隐私预算",
      type: "gauge",
      progress: {
        show: true,
      },
      detail: {
        valueAnimation: true,
        formatter: "{value}",
      },
      min: 0,
      max: realPrivacyBudget.value*2,
      data: [
        {
          value: realPrivacyBudget.value,
          name: "真实值",
        },
      ],
    },
  ],
});

let chart;
let chartRef = ref(null);

// 添加新的图表配置和初始化代码
const realChartRef = ref(null);
let realChart;

onMounted(() => {
  animateEstimatedBudget();
  
  // 初始化两个图表
  realChart = echarts.init(realChartRef.value);
  realChart.setOption(realOption.value);
  
  chart = echarts.init(chartRef.value);
  chart.setOption(estimatedOption.value);
});

// 在 onUnmounted 中清理两个图表
onUnmounted(() => {
  if (chart) {
    chart.dispose();
  }
  if (realChart) {
    realChart.dispose();
  }
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