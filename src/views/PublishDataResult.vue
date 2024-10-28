<template>
  <el-container class="publish-data-result-container">
    <el-main>
      <el-card class="mb-4">
        <template #header>
          <h1>数据发布结果</h1>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item v-for="(value, key) in formattedParams" :key="key" :label="key">
            {{ value }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card class="mb-4" v-if="chartData">
        <template #header>
          <h2>数据可视化</h2>
        </template>
        <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
      </el-card>

      <el-button type="primary" @click="goBack">返回</el-button>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import * as echarts from 'echarts';

const router = useRouter();
const params = ref({});
const chartContainer = ref(null);
let chart = null;

const formattedParams = computed(() => {
  const formatted = {};
  for (const [key, value] of Object.entries(params.value)) {
    if (typeof value === 'object' && value !== null) {
      formatted[key] = JSON.stringify(value, null, 2);
    } else {
      formatted[key] = value;
    }
  }
  return formatted;
});

const chartData = computed(() => {
  // 这里添加处理图表数据的逻辑
  // 示例：
  if (params.value.data) {
    return params.value.data.map(item => ({
      name: item.category,
      value: item.value
    }));
  }
  return null;
});

const initChart = () => {
  if (chartData.value && chartContainer.value) {
    chart = echarts.init(chartContainer.value);
    const option = {
      title: {
        text: '数据分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      series: [
        {
          name: '数据类别',
          type: 'pie',
          radius: '50%',
          data: chartData.value,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };
    chart.setOption(option);
  }
};

const getQueryParams = () => {
  const queryParams = {};
  const searchParams = new URLSearchParams(window.location.search);
  for (const [key, value] of searchParams.entries()) {
    try {
      queryParams[key] = JSON.parse(value);
    } catch {
      queryParams[key] = value;
    }
  }
  return queryParams;
};

const goBack = () => {
  router.push('/publishData');
};

onMounted(() => {
  params.value = getQueryParams();
  initChart();

  window.addEventListener('resize', () => {
    if (chart) {
      chart.resize();
    }
  });
});
</script>

<style scoped>
.publish-data-result-container {
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

.el-descriptions {
  margin-top: 20px;
}

.el-button {
  margin-top: 20px;
}
</style>