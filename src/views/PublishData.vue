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
          <el-form-item label="隐私列">
            <el-select v-model="formData.prv" multiple placeholder="请选择隐私列">
              <el-option v-for="col in tableColumns1" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>

          <el-form-item label="准标识符列">
            <el-select v-model="formData.pub" multiple placeholder="请选择准标识符列">
              <el-option v-for="col in tableColumns1" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>

          <el-form-item label="标识符列">
            <el-select v-model="formData.index" multiple placeholder="请选择标识符列">
              <el-option v-for="col in tableColumns1" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item>

          <!-- <el-form-item label="其他">
            <el-select v-model="formData.others" multiple placeholder="请选择其他列">
              <el-option v-for="col in tableColumns1" :key="col" :label="col" :value="col" />
            </el-select>
          </el-form-item> -->
        </el-card>

        <el-card class="mb-4">
          <el-form-item label="选择算法">
            <el-radio-group v-model="formData.alg">
              <el-radio value="k">k-匿名</el-radio>
              <el-radio value="l">l-多样性</el-radio>
              <el-radio value="t">t-closeness</el-radio>
              <el-radio value="dp">差分隐私</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-card>

        <el-form-item>
          <el-button type="primary" native-type="submit">提交</el-button>
        </el-form-item>
      </el-form>

      <el-button class="mt-4" type="primary">
        <router-link to="/" class="link">本地数据</router-link>
      </el-button>
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
import { ref, reactive } from 'vue';
import { ElMessage, ElDialog, ElProgress } from 'element-plus';
import * as XLSX from 'xlsx';
import router from '@/router';

const tableData1 = ref([]);
const tableData2 = ref([]);
const tableColumns1 = ref([]);
const tableColumns2 = ref([]);
const currentPage1 = ref(1);
const currentPage2 = ref(1);
const pageSize = 10;

const isProcessing = ref(false);
const processingPercentage = ref(0);
const processingMessage = ref('正在提交数据...');

const csrfToken = ref('x5Wc4PBB83vmwmBikZViTClc5Ol42aQmlQKyNNqKviMPeSnCWw5Ju4pqsAtsFv2z');

const formData = reactive({
  prv: [],
  pub: [],
  index: [],
  // others: [],
  alg: ''
});

const base_url = 'http://localhost:8000/api/';

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

  console.log("debug 232323 ", formData)
  try {
    isProcessing.value = true;
    processingPercentage.value = 0;
    processingMessage.value = '正在提交数据...';

    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (processingPercentage.value < 90) {
        processingPercentage.value += 10;
      }
    }, 500);

    const response = await fetch(base_url + url, {
      headers: {
        'Content-Type': 'application/json', // 设置请求头为 JSON
      },
      method: 'POST',
      body: JSON.stringify(formData),
    });

    clearInterval(progressInterval);

    if (!response.ok) {
      throw new Error('网络响应不正常');
    }

    const data = await response.json();
    console.log('Success:', data);

    processingPercentage.value = 100;
    processingMessage.value = '处理完成!';

    // 短暂延迟后关闭模态框并跳转
    setTimeout(() => {
      isProcessing.value = false;
      router.push({ path: '/publishDataResult', query: data });
    }, 1000);

  } catch (error) {
    console.error('Error:', error);
    processingMessage.value = '处理出错,请重试';
    ElMessage.error('表单提交失败，请重试');
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