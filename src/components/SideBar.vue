<template>
  <div class="sidebar-container">
    <el-scrollbar>
      <el-menu class="sidebar-menu" default-active="1" :collapse="isCollapse" @open="handleOpen" @close="handleClose"
        :default-openeds="['6']">
        <el-menu-item index="1" @click="selectForm('ob_measureDiv', 'ob_measure')">
          <span>第一类：通用的数据采集算法评估</span>
        </el-menu-item>

        <el-sub-menu index="2">
          <template #title>
            <span>第二类：数值型数据采集算法评估</span>
          </template>
          <el-menu-item v-for="algo in numericalAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_numericalDiv', algo.name)">
            {{ algo.name + "&nbsp;机制" }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <span>第三类：类别型数据采集算法评估</span>
          </template>
          <el-menu-item v-for="algo in discreteAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_discreteDiv', algo.name)">
            {{ algo.name + "&nbsp;机制" }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <span>第四类：集合型数据采集算法评估</span>
          </template>
          <el-menu-item v-for="algo in setAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_setDiv', algo.name)">
            {{ algo.name + "&nbsp;机制" }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5">
          <template #title>
            <span>第五类：键-值型数据采集算法评估</span>
          </template>
          <el-menu-item v-for="algo in keyValueAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_key_valueDiv', algo.name)">
            {{ algo.name + "&nbsp;机制" }}
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="6" @click="handlePublishMode('null')">
          第六类：通用的数据发布算法评估
        </el-menu-item>

         <el-menu-item index="7" @click="handlePublishMode('k')">
           第七类：k-匿名数据发布算法评估
         </el-menu-item>

        <el-menu-item index="8" @click="handlePublishMode('l')">
           第八类：l-多样性数据发布算法评估
        </el-menu-item>

        <el-menu-item index="9" @click="handlePublishMode('t')">
          第九类：t-closeness数据发布算法评估
        </el-menu-item>

      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';
import { ref } from 'vue';
import { ElMenu, ElMenuItem, ElSubMenu } from 'element-plus';

const emit = defineEmits(['select-form', 'publish-mode']);

const selectForm = (formType, algName) => {
  emit('publish-mode', "collection_mode");
  emit('select-form', formType, algName);
};

// 新增发布模式处理函数
const handlePublishMode = (mode) => {
  emit('publish-mode', mode);
};

const isCollapse = ref(false);

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};

const numericalAlgorithms = [
  { name: 'Duchi' },
  { name: 'PM' },
  { name: 'Laplace' }
];

const discreteAlgorithms = [
  { name: 'RR' },
  { name: 'SUE' },
  { name: 'OUE' },
  { name: 'BLH' },
  { name: 'OLH' },
  { name: 'HE' },
  // { name: 'k-Subset' }
];

const keyValueAlgorithms = [
  { name: 'PrivKVM' },
  { name: 'PCKV-UE' },
  { name: 'PCKV-GRR' }
];

const setAlgorithms = [
  // { name: 'd-PAPPOR' },
  // { name: 'OLHSampling' },
  // { name: 'OUESampling' },
  { name: 'PrivSet' },
  { name: 'Wheel' },
  // { name: 'LdpMinner' }
];
</script>

<style scoped>
.sidebar-container {
  height: 100vh;
  background-color: #f0f2f5;
  transition: all 0.3s;
}

.sidebar-menu {
  border-right: none;
  transition: width 0.3s;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 300px;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 56px;
  line-height: 56px;
}

:deep(.el-menu-item.is-active) {
  background-color: #e6f7ff;
  border-right: 3px solid #1890ff;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background-color: #f6f6f6;
}

.collapse-btn {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.collapse-btn .el-icon {
  font-size: 20px;
  color: #909399;
}

.collapse-btn .el-icon.is-active {
  transform: rotate(180deg);
}

:deep(.el-scrollbar__wrap) {
  overflow-x: hidden;
}

.publish-link {
  text-decoration: none;
  color: inherit;
}
</style>