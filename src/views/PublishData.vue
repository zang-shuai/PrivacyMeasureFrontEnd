<template>
  <el-container class="publish-data-container">
    <el-aside width="40%">
      <el-form id="submitDataForm" :model="formData" label-position="top"
        @submit.prevent="submitForm('submitDataForm', 'submitdata_measure')">
        <el-input type="hidden" name="csrfmiddlewaretoken" v-model="csrfToken" />

        <el-card class="mb-4">
          <el-form-item label="原始数据">
            <el-upload action="#" :auto-upload="false" :on-change="(file) => handleFile(file, 'output1')"
              accept=".xls, .xlsx, .csv">
              <el-button type="primary">选择文件</el-button>
            </el-upload>
          </el-form-item>
        </el-card>

        <el-card class="mb-4">
          <el-form-item label="处理后数据">
            <el-upload action="#" :auto-upload="false" :on-change="(file) => handleFile(file, 'output2')"
              accept=".xls, .xlsx, .csv">
              <el-button type="primary">选择文件</el-button>
            </el-upload>
          </el-form-item>
        </el-card>

        <el-card class="mb-4">
          <el-form-item label="标识符列">
            <el-select v-model="formData.index" multiple placeholder="请选择标识符列">
              <el-option v-for="col in tableColumns1" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>

          <el-form-item label="准标识符列">
            <el-select v-model="formData.pub" multiple placeholder="请选择准标识符列">
              <el-option v-for="col in availableColumns" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>

          <el-form-item label="隐私列">
            <el-select v-model="formData.prv" multiple placeholder="请选择隐私列">
              <el-option v-for="col in availableColumns" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>
        </el-card>

<!--        <el-card class="mb-4">-->
<!--          <el-form-item label="选择算法">-->
<!--            <el-radio-group v-model="formData.alg">-->
<!--              <el-radio value="k">k-匿名</el-radio>-->
<!--              <el-radio value="l">l-多样性</el-radio>-->
<!--              <el-radio value="t">t-closeness</el-radio>-->
<!--              &lt;!&ndash;              <el-radio value="dp">差分隐私</el-radio>&ndash;&gt;-->
<!--              <el-radio value="null">未知</el-radio>-->
<!--            </el-radio-group>-->
<!--          </el-form-item>-->
<!--        </el-card>-->

        <el-form-item>
          <el-button type="primary" native-type="submit">提交</el-button>
        </el-form-item>
      </el-form>

<!--      <el-button class="mt-4" type="primary">-->
<!--        <router-link to="/" class="link">本地差分隐私模式</router-link>-->
<!--      </el-button>-->
    </el-aside>

    <el-main>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="mb-4">
            <template #header>
              <div class="card-header">
                <span>原始数据</span>
              </div>
            </template>
            <div id="output1" class="output-container">
              <el-table :data="tableData1.slice((currentPage1 - 1) * pageSize, currentPage1 * pageSize)" height="100%">
                <el-table-column v-for="(col, index) in tableColumns1" :key="index" :prop="col" :label="col" />
              </el-table>
              <el-pagination @current-change="handleCurrentChange1" :current-page="currentPage1" :page-size="pageSize"
                :total="tableData1.length" layout="prev, pager, next" />
            </div>
          </el-card>
        </el-col>
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>处理后数据</span>
              </div>
            </template>
            <div id="output2" class="output-container">
              <el-table :data="tableData2.slice((currentPage2 - 1) * pageSize, currentPage2 * pageSize)" height="100%">
                <el-table-column v-for="(col, index) in tableColumns2" :key="index" :prop="col" :label="col" />
              </el-table>
              <el-pagination @current-change="handleCurrentChange2" :current-page="currentPage2" :page-size="pageSize"
                :total="tableData2.length" layout="prev, pager, next" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>

  <el-dialog v-model="isProcessing" title="数据处理中" width="30%" :close-on-click-modal="false"
    :close-on-press-escape="false" :show-close="false">
    <div class="processing-content">
      <el-progress type="circle" :percentage="processingPercentage" />
      <p>{{ processingMessage }}</p>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { ElMessage, ElDialog, ElProgress } from 'element-plus';
import * as XLSX from 'xlsx';
import router from '@/router';

const tableData1 = ref([]);
const tableData2 = ref([]);
const tableColumns1 = ref([]);
const tableColumns2 = ref([]);

const availableColumns = computed(() => {
  return tableColumns1.value.filter(col => !formData.index.includes(col));
});

const currentPage1 = ref(1);
const currentPage2 = ref(1);
const pageSize = 10;

// 添加文件存储变量
const file1 = ref(null);
const file2 = ref(null);

const isProcessing = ref(false);
const processingPercentage = ref(0);
const processingMessage = ref('正在提交数据...');

const csrfToken = ref('x5Wc4PBB83vmwmBikZViTClc5Ol42aQmlQKyNNqKviMPeSnCWw5Ju4pqsAtsFv2z');

const formData = reactive({
  prv: [],
  pub: [],
  index: [],
  // others: [],
  alg: 'null'
});

const base_url = 'http://localhost:8000/api/';

// 检查表单数据是否填满
// const isFormValid = computed(() => {
//   return formData.prv.length > 0 && formData.pub.length > 0  && formData.alg.length  > 0;
// });

// 监听标识符列的变化
watch(() => formData.index, (newVal) => {
  // 从隐私列和准标识符列中移除已选为标识符的列
  formData.prv = formData.prv.filter(col => !newVal.includes(col));
  formData.pub = formData.pub.filter(col => !newVal.includes(col));
}, { deep: true });

const handleCurrentChange1 = (val) => {
  currentPage1.value = val;
};

const handleCurrentChange2 = (val) => {
  currentPage2.value = val;
};

const handleFile = (file, outputId) => {
  const reader = new FileReader();
  reader.onload = (event) => {
    const data = new Uint8Array(event.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
    const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });

    if (outputId === 'output1') {
      file1.value = file.raw;  // 保存文件对象
      tableColumns1.value = jsonData[0];
      tableData1.value = jsonData.slice(1).map(row => {
        const rowData = {};
        tableColumns1.value.forEach((col, index) => {
          rowData[col] = row[index];
        });
        return rowData;
      });

      formData.prv = [...tableColumns1.value];
      formData.pub = [...tableColumns1.value];
      formData.index = [...tableColumns1.value];
      // formData.others = [...tableColumns1.value];
    } else {
      file2.value = file.raw;  // 保存文件对象
      tableColumns2.value = jsonData[0];
      tableData2.value = jsonData.slice(1).map(row => {
        const rowData = {};
        tableColumns2.value.forEach((col, index) => {
          rowData[col] = row[index];
        });
        return rowData;
      });
    }
  };
  reader.readAsArrayBuffer(file.raw);
};

const submitForm = async (formId, url) => {
  // 如果文件未上传，则显示错误消息并退出函数
  if (!file1.value || !file2.value) {
    ElMessage.error('请先上传两个文件'); // 提示用户上传文件
    return; // 终止函数执行
  }
  if (formData.prv.length > 0 && formData.pub.length > 0) {
    try {
      console.log('formData:', formData); // 打印表单数据到控制台
      // 初始化处理状态
      isProcessing.value = true; // 标记正在处理
      processingPercentage.value = 0; // 初始化进度条为 0%
      processingMessage.value = '正在提交数据...'; // 显示提交消息
      console.log('正在提交数据...');
      if (file1.value.size > 156644) {
        processingMessage.value = '正在提交，数据量较大，请耐心等待，约需 ' + toString(file1.value.size / 40000 / 60) + ' 分钟'; // 显示提交消息
      }

      // 创建 FormData 对象用于存储表单数据
      const formDataToSend = new FormData();

      // 添加上传的文件到 FormData
      formDataToSend.append('originFile', file1.value); // 添加原始文件
      formDataToSend.append('handledFile', file2.value); // 添加处理后的文件

      // 检查表单字段是否为空，如果为空则使用默认值 ['index']
      const processedPrv = formData.prv.length === 0 ? ['index'] : formData.prv;
      const processedPub = formData.pub.length === 0 ? ['index'] : formData.pub;
      const processedIndex = formData.index.length === 0 ? ['index'] : formData.index;

      // 将其他表单字段添加到 FormData，字段数据转换为 JSON 字符串
      formDataToSend.append('prv', JSON.stringify(processedPrv)); // 私有字段
      formDataToSend.append('pub', JSON.stringify(processedPub)); // 公有字段
      formDataToSend.append('index', JSON.stringify(processedIndex)); // 索引字段
      formDataToSend.append('alg', formData.alg); // 算法选项

      // 模拟进度更新，每 500 毫秒增加进度条
      const progressInterval = setInterval(() => {
        if (processingPercentage.value < 90) {
          processingPercentage.value += 10; // 逐步增加进度
        }
      }, 500);

      // 使用 fetch 向后端提交表单数据
      const response = await fetch(base_url + url, {
        method: 'POST', // 使用 POST 方法
        body: formDataToSend, // 提交数据
      });

      // 清除进度条的定时器，避免重复执行
      clearInterval(progressInterval);

      // 如果后端返回的状态码不是成功的范围，则抛出错误
      if (!response.ok) {
        throw new Error('网络响应不正常'); // 抛出错误以进入 catch 块
      }

      // 解析后端返回的 JSON 数据
      const data = await response.json();
      console.log('Success:', data); // 打印返回的数据到控制台

      // 设置进度条为 100% 并更新处理状态消息
      processingPercentage.value = 100;
      processingMessage.value = '处理完成!';

      // 将后端返回的数据与附加信息合并，用于结果展示页面
      const transformData = {
        ...data, // 展开后端返回的数据
        others: {
          prv: processedPrv, // 包含私有字段信息
          pub: processedPub, // 包含公有字段信息
          index: processedIndex, // 包含索引字段信息
        },
      };

      // 设置短暂延迟后，跳转到结果展示页面并传递数据
      setTimeout(() => {
        isProcessing.value = false; // 重置处理状态
        router.push({
          path: '/publishDataResult', state: {
            data: encodeURIComponent(JSON.stringify(transformData)), // 序列化并编码
          }
        }); // 跳转到结果页面
        // 使用 query 参数
        router.push({
          path: '/publishDataResult', query: {
            data: encodeURIComponent(JSON.stringify(transformData)), // 序列化并编码
          }
        });
      }, 1000);

    } catch (error) {
      // 捕获并处理错误
      console.error('Error:', error); // 打印错误日志
      processingMessage.value = '处理出错,请重试'; // 显示错误信息
      ElMessage.error('表单提交失败，请重试'); // 提示用户提交失败
    }
  } else {
    if (formData.pub.length === 0) {
      ElMessage.error('请选择准标识符列');
    } else if (formData.prv.length === 0) {
      ElMessage.error('请选择隐私列');
    }
  }
};


</script>

<style scoped>
.publish-data-container {
  display: flex;
  height: 100vh;
}

.el-aside {
  padding: 20px;
  border-right: 1px solid #dcdfe6;
  overflow-y: auto;
}

.el-main {
  padding: 20px;
  overflow-y: auto;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 16px;
}

.output-container {
  height: calc(50vh - 60px);
  overflow: auto;
}

.output-container .el-table {
  height: calc(100% - 40px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.link {
  text-decoration: none;
  color: inherit;
}
</style>