<template>
  <div class="sidebar-container">
    <el-scrollbar>
      <el-menu class="sidebar-menu" default-active="1" :collapse="isCollapse" @open="handleOpen" @close="handleClose">
        <el-menu-item index="1" @click="selectForm('ob_measureDiv', 'ob_measure')">
          <span>第一类：未知数据采集算法</span>
        </el-menu-item>

        <el-sub-menu index="2">
          <template #title>
            <span>第二类：数值型数据采集算法</span>
          </template>
          <el-menu-item v-for="algo in numericalAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_numericalDiv', algo.name)">
            {{ algo.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <span>第三类：类别型数据采集算法</span>
          </template>
          <el-menu-item v-for="algo in discreteAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_discreteDiv', algo.name)">
            {{ algo.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <span>第五类：key-value型数据采集算法</span>
          </template>
          <el-menu-item v-for="algo in keyValueAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_key_valueDiv', algo.name)">
            {{ algo.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5">
          <template #title>
            <span>第四类：集合型数据采集算法</span>
          </template>
          <el-menu-item v-for="algo in setAlgorithms" :key="algo.name" :index="algo.name"
            @click="selectForm('ab_setDiv', algo.name)">
            {{ algo.name }}
          </el-menu-item>
        </el-sub-menu>

        <!-- <el-menu-item index="6">
          <router-link to="/publishData" class="publish-link" style="display: block; width: 100%; height: 100%;">
            发布数据模式
          </router-link>
        </el-menu-item> -->
        <el-sub-menu index="6">
          <template #title>
            <span>发布数据模式</span>
          </template>
          <el-menu-item index="6-1" @click="selectForm('pb_unknownDiv', 'pb_unknown')">
            <router-link to="/publishData" class="publish-link" style="display: block; width: 100%; height: 100%;">
              第六类：未知数据发布算法
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-2" @click="selectForm('pb_kanonymityDiv', 'pb_kanonymity')">
            <router-link to="/publishData" class="publish-link" style="display: block; width: 100%; height: 100%;">
              第七类：k-匿名数据发布算法
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-3" @click="selectForm('pb_ldiversityDiv', 'pb_ldiversity')">
            <router-link to="/publishData" class="publish-link" style="display: block; width: 100%; height: 100%;">
              第八类：l-多样性数据发布算法
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-4" @click="selectForm('pb_tclosenessDiv', 'pb_tcloseness')">
            <router-link to="/publishData" class="publish-link" style="display: block; width: 100%; height: 100%;">
              第九类：t-接近性数据发布算法
            </router-link>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';
import { ref } from 'vue';
import { ElMenu, ElMenuItem, ElSubMenu } from 'element-plus';

const emit = defineEmits(['select-form']);

const selectForm = (formType, algName) => {
  emit('select-form', formType, algName);
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
  width: 250px;
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