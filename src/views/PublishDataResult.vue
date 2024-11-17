<template>
  <el-container class="publish-data-result-container">
    <el-main>
      <el-card class="mb-4">
        <template #header>
          <h1>整体隐私度量结果</h1>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="整体隐私泄露风险">
            <span :class="getRiskClass(params.data?.PLS?.all)">
              {{ params.data?.PLS?.all?.toFixed(4) }}
            </span>
            <el-tag :type="getTagType(params.data?.PLS?.all)" style="margin-left: 10px">
              {{ getStatus(params.data?.PLS?.all) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="参数设置" v-show="params.data?.PLS?.para!=='null'">
            {{ params.data?.PLS?.para }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      <!--      <el-row :gutter="20" class="mb-4">-->
      <!--        <el-col>-->
      <el-card class="mb-4">
        <div style="justify-content: center;">
          <div class="echarts" ref="chart2Ref" style="width: 100%; height: 400px;"></div>
        </div>
      </el-card>
      <!--        </el-col>-->
      <!--      </el-row>-->

      <el-card class="mb-4">
        <template #header>
          <h1>数据列分类结果</h1>
        </template>

        <el-descriptions :column="1" border>
          <!--          <el-descriptions-item label="标识符列">
                      <div ref="entropyChartContainer" style="width: 100%; height: 400px;"></div>
                      <el-table :data="entropyTableData" stripe style="margin-top: 20px;">
                        <el-table-column prop="column" label="列名"/>
                        <el-table-column prop="value" label="熵值">
                          <template #default="scope">
                            <span :class="getRiskClass(scope.row.value)">{{ scope.row.value.toFixed(4) }}</span>
                          </template>
                        </el-table-column>
                        <el-table-column prop="plsValue" label="度量值">
                          <template #default="scope">
                            <span :class="getRiskClass(scope.row.plsValue)">{{ scope.row.plsValue.toFixed(4) }}</span>
                          </template>
                        </el-table-column>
                        <el-table-column prop="status" label="状态">
                          <template #default="scope">
                            <el-tag :type="getTagType(scope.row.value)">{{ getStatus(scope.row.value) }}</el-tag>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-descriptions-item>-->
          <el-descriptions-item label="准标识符列">
            <div ref="quasiChartContainer" style="width: 100%; height: 400px;"></div>
            <el-table :data="quasiTableData" stripe style="margin-top: 20px;">
              <el-table-column prop="column" label="列名"/>
              <el-table-column prop="value" label="熵值">
                <template #default="scope">
                  <span :class="getRiskClass(scope.row.value)">{{ scope.row.value.toFixed(4) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="plsValue" label="度量值">
                <template #default="scope">
                  <span :class="getRiskClass(scope.row.plsValue)">{{ scope.row.plsValue.toFixed(4) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag :type="getTagType(scope.row.value)">{{ getStatus(scope.row.value) }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-descriptions-item>
          <el-descriptions-item label="隐私列">
            <div ref="privacyChartContainer" style="width: 100%; height: 400px;"></div>
            <el-table :data="privacyTableData" stripe style="margin-top: 20px;">
              <el-table-column prop="column" label="列名"/>
              <el-table-column prop="value" label="熵值">
                <template #default="scope">
                  <span :class="getRiskClass(scope.row.value)">{{ scope.row.value.toFixed(4) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="plsValue" label="度量值">
                <template #default="scope">
                  <span :class="getRiskClass(scope.row.plsValue)">{{ scope.row.plsValue.toFixed(4) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag :type="getTagType(scope.row.value)">{{ getStatus(scope.row.value) }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card class="mb-4" v-if="params.PLS">
        <template #header>
          <h2>隐私泄露风险评估</h2>
        </template>
        <div class="risk-analysis">
          <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
          <div class="risk-legend">
            <div class="risk-item good">
              <span class="dot"></span>良好 (0-0.3333)
            </div>
            <div class="risk-item moderate">
              <span class="dot"></span>合格 (0.3333-0.6666)
            </div>
            <div class="risk-item risk">
              <span class="dot"></span>有风险 (>0.6666)
            </div>
          </div>
          <el-table :data="plsTableData" stripe style="margin-top: 20px;">
            <el-table-column prop="column" label="列名"/>
            <el-table-column prop="value" label="PLS值">
              <template #default="scope">
                <span :class="getRiskClass(scope.row.value)">{{ scope.row.value.toFixed(4) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="getTagType(scope.row.value)">{{ getStatus(scope.row.value) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <el-button type="primary" @click="goBack">返回</el-button>
    </el-main>
  </el-container>
</template>

<script setup>
import {ref, onMounted, computed, onUnmounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import * as echarts from 'echarts';
import {ElMessage} from 'element-plus';

const router = useRouter();
const params = ref({});
const chartContainer = ref(null);
let chart = null;
const quasiChartContainer = ref(null);
const privacyChartContainer = ref(null);
let quasiChart = null;
let privacyChart = null;

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

const plsTableData = computed(() => {
  if (!params.value.PLS) return [];
  return Object.entries(params.value.PLS).map(([column, value]) => ({
    column,
    value,
    status: getStatus(value)
  }));
});

const quasiTableData = computed(() => {
  if (!params.value?.data?.PLS) return [];
  return Object.entries(params.value.data.PLS)
      .filter(([column]) => params.value.others.pub?.includes(column))
      .map(([column, value]) => ({
        column,
        value,
        plsValue: params.value.data.PLS[column],
        status: getStatus(value)
      }));
});

const privacyTableData = computed(() => {
  if (!params.value?.data?.PLS) return [];
  return Object.entries(params.value.data.PLS)
      .filter(([column]) => params.value.others.prv?.includes(column))
      .map(([column, value]) => ({
        column,
        value,
        plsValue: params.value.data.PLS[column],
        status: getStatus(value)
      }));
});

const entropyTableData = computed(() => {
  if (!params.value?.data?.PLS) return [];
  return Object.entries(params.value.data.PLS)
      .filter(([column]) => params.value.others.index?.includes(column))
      .map(([column, value]) => ({
        column,
        value,
        plsValue: params.value.data.PLS[column],
        status: getStatus(value)
      }));
});


const getStatus = (value) => {
  if (value <= 0.3333) return '良好';
  if (value <= 0.6666) return '合格';
  return '有风险';
};

const getTagType = (value) => {
  if (value <= 0.3333) return 'success';
  if (value <= 0.6666) return 'warning';
  return 'danger';
};

const getRiskClass = (value) => {
  if (value <= 0.3333) return 'text-success';
  if (value <= 0.6666) return 'text-warning';
  return 'text-danger';
};


const entropyChartContainer = ref(null);
let entropyChart = null;

const initChart = () => {
  if (params.value.PLS && chartContainer.value) {
    chart = echarts.init(chartContainer.value);
    const data = Object.entries(params.value.PLS).map(([name, value]) => ({
      name,
      value: Number(value.toFixed(4))
    }));

    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.name),
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        max: 1,
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      series: [{
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: item.value <= 0.3333 ? '#67C23A' :
                item.value <= 0.6666 ? '#E6A23C' : '#F56C6C'
          }
        })),
        type: 'bar',
        barWidth: '30%',
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }],
      visualMap: {
        show: false,
        pieces: [{
          gt: 0.6666,
          color: '#F56C6C'
        }, {
          gt: 0.3333,
          lte: 0.6666,
          color: '#E6A23C'
        }, {
          lte: 0.3333,
          color: '#67C23A'
        }]
      }
    };
    chart.setOption(option);
  }
};

const initCharts = () => {
  // 原有的 PLS 图表初始化
  initChart();

  // 创建图表的通用函数
  const createEntropyChart = (container, data) => {
    if (!container) return null;
    const chart = echarts.init(container);
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.name),
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      series: [{
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: item.value <= 0.3333 ? '#67C23A' :
                item.value <= 0.6666 ? '#E6A23C' : '#F56C6C'
          }
        })),
        type: 'bar',
        barWidth: '30%',
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }]
    };
    chart.setOption(option);
    return chart;
  };

  // 初始化标识符列图表
  if (params.value?.data?.PLS && entropyChartContainer.value) {
    const data = Object.entries(params.value.data.PLS)
        .filter(([column]) => params.value.others.index?.includes(column))
        .map(([name, value]) => ({
          name,
          value: Number(value.toFixed(4))
        }));
    entropyChart = createEntropyChart(entropyChartContainer.value, data);
  }

  // 初始化准标识符列图表
  if (params.value?.data?.PLS && quasiChartContainer.value) {
    const data = Object.entries(params.value.data.PLS)
        .filter(([column]) => params.value.others.pub?.includes(column))
        .map(([name, value]) => ({
          name,
          value: Number(value.toFixed(4))
        }));
    quasiChart = createEntropyChart(quasiChartContainer.value, data);
  }

  // 初始化隐私列图表
  if (params.value?.data?.PLS && privacyChartContainer.value) {
    const data = Object.entries(params.value.data.PLS)
        .filter(([column]) => params.value.others.prv?.includes(column))
        .map(([name, value]) => ({
          name,
          value: Number(value.toFixed(4))
        }));
    privacyChart = createEntropyChart(privacyChartContainer.value, data);
  }
};

const goBack = () => {
  router.push('/publishData');
};


const option2 = ref({
  tooltip: {
    formatter: "{a} <br/>{b} : {c}%",
  },
  series: [
    {
      name: "Pressure",
      type: "gauge",
      progress: {
        show: true,
      },
      detail: {
        valueAnimation: true,
        formatter: "{value}",
      },

      axisLine: {
        lineStyle: {
          // width: 30,'#E6A23C' : '#F56C6C'
          color: [[0.33, '#67C23A'], [0.66, '#E6A23C'], [1, '#F56C6C']]
        }
      },
      min: 0, // 最小刻度
      max: 1, // 最大刻度
      data: [
        {
          // value: parseFloat(params.data?.PLS?.all.toFixed(2)),
          // value: params.data?.PLS?.all,
          value: 0.5,
          name: "SCORE",
        },
      ],
    },
  ],
});

let chart2;
let chart2Ref = ref(null);


onMounted(() => {
  const route = useRoute();
  console.log(route.query);
  params.value = JSON.parse(decodeURIComponent(route.query.data));
  console.log(params.value);
  if (params.value.message === 'fail') {
    // 展示错误信息
    ElMessage.error(params.value.data);
    return;
  }
  initCharts();
  window.addEventListener('resize', () => {
    if (chart) {
      chart.resize();
    }
    if (entropyChart) {
      entropyChart.resize();
    }
  });


  chart2 = echarts.init(chart2Ref.value)
  chart2.setOption(option2.value)
});

onUnmounted(() => {
  if (chart) chart.dispose();
  if (entropyChart) entropyChart.dispose();
  if (quasiChart) quasiChart.dispose();
  if (privacyChart) privacyChart.dispose();
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

.risk-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.risk-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.good .dot {
  background-color: #67C23A;
}

.moderate .dot {
  background-color: #E6A23C;
}

.risk .dot {
  background-color: #F56C6C;
}

.text-success {
  color: #67C23A;
}

.text-warning {
  color: #E6A23C;
}

.text-danger {
  color: #F56C6C;
}

.publish-data-result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-descriptions-item {
  padding: 20px;
}

.el-tag {
  margin-left: 10px;
}
</style>