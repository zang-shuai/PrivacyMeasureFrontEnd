<template>
  <el-form :model="formData" @submit.prevent="submitForm" class="main-content">
    <el-card class="algorithm-card">
      <template #header>
        <div class="card-header">
          <h2 class="algorithm-title">{{ formData.alg_name.content === "ob_measure" ? "通用的数据采集算法评估" :
            formData.alg_name.content + "&nbsp;机制" }}
          </h2>
        </div>
      </template>

      <div class="card-body">
        <FormField v-if="showField('input_type')" id="input_type">
          <el-form-item label="输入类型:">
            <el-radio-group v-model="formData.input_type.content">
              <el-radio-button v-for="option in inputTypeOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
        </FormField>

        <FormField
          v-if="showField('discrete_domain') || (formData.alg_type.content === 'ob_measureDiv' && formData.input_type.content === 'single_discrete_input')"
          id="discrete_domain" class="mb-4">
          <el-form-item label="离散输入域:">
            <el-input id="discrete_domain_input" v-model="formData.discrete_domain.content"
              placeholder="请输入兼容 python 代码的列表" />
          </el-form-item>
        </FormField>

        <FormField
          v-if="showField('continue_min_domain') || (formData.alg_type.content === 'ob_measureDiv' && formData.input_type.content === 'single_continuous_input')"
          class="input-range mb-4">
          <el-form-item label="连续输入范围:">
            <el-input-number v-model="formData.continue_min_domain.content" :min="0"
              :max="formData.continue_max_domain.content" placeholder="最小值" />
            <span class="range-separator">至</span>
            <el-input-number v-model="formData.continue_max_domain.content" :min="formData.continue_min_domain.content"
              placeholder="最大值" />
          </el-form-item>
        </FormField>

        <FormField
          v-if="showField('set_size_domain') || (formData.alg_type.content == 'ob_measureDiv' && formData.input_type.content == 'discrete_set_input')"
          class="d-flex align-items-center mb-2">
          <el-form-item label="输入集合大小：">
            <el-input v-model="formData.set_size_domain.content" />
          </el-form-item>
          <el-form-item label="集合输入域：">
            <el-input v-model="formData.set_domain.content" />
          </el-form-item>
        </FormField>

        <FormField
          v-if="showField('key_domain') || (formData.alg_type.content == 'ob_measureDiv' && formData.input_type.content == 'key_value_input')"
          class="d-flex align-items-center mb-2">
          <el-form-item label="key的输入域：">
            <el-input v-model="formData.key_domain.content" />
          </el-form-item>
        </FormField>

        <FormField class="mb-4">
          <el-form-item>
            <div class="content">
              <div v-if="showField('value_domain')" id="value_domain" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="value_domain_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">value的输入域：
                    <span>[-1, 1]</span></label>
                </div>
              </div>
            </div>
          </el-form-item>
        </FormField>

        <FormField v-if="showField('output_type')" id="output_type">
          <el-form-item label="输出类型:">
            <el-radio-group v-model="formData.output_type.content">
              <el-radio-button v-for="option in outputTypeOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
        </FormField>

        <FormField class="mb-4">
          <el-form-item>
            <div class="content">
              <el-radio-group v-model="selectedMethod" @change="changeMethod">
                <el-radio-button v-for="method in callMethods" :key="method.value" :value="method.value">
                  {{ method.label }}
                </el-radio-button>
              </el-radio-group>

              <!-- code 算法代码 -->
              <div v-show="showField('code_file')" id="code_file" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="code_file_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">算法代码：</label>
                  <el-input type="textarea" id="code_file_input" name="code" cols="100" rows="15"
                    v-model="formData.code_file.content" class="form-control ms-2"></el-input>
                </div>
              </div>


              <!-- exe_file 算法可执行文件 -->
              <div v-if="showField('exe_file')" id="exe_file" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="exe_file_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">请上传算法的可执行文件：</label>
                  <el-upload class="upload-demo" :action="'#'" :auto-upload="false" :on-change="handleFileChange"
                    :limit="1">
                    <el-button size="small" type="primary">选择文件</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        只能上传一个可执行文件
                      </div>
                    </template>
                  </el-upload>
                </div>
              </div>


              <!-- api_file 算法调用 api -->
              <div v-if="showField('api_file')" id="api_file" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="api_file_input" class="form-label text-muted mb-2" style="white-space: nowrap">
                    算法调用url：
                  </label>
                  <el-input id="api_file_input" name="api_file" v-model="formData.api_file.content" type="text"
                    required="true" class="form-control ms-2">
                  </el-input>
                </div>
              </div>


              <!-- 第一类：通用的数据采集算法评估 算法输入输出参数格式 -->
              <div v-if="showField('ob_format')" id="ob_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="ob_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">第一类：通用的数据采集算法评估算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="ob_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">第一类：通用的数据采集算法评估算法输出格式：<span>
                      <!--                      <pre>-->
                      <!--                  {-->
                      <!--                  # 编码值列表-->
                      <!--                  "encode_list": [...],-->
                      <!--                  # 扰动值列表-->
                      <!--                  "perturb_list": [...]-->
                      <!--                  }</pre>-->
                      <pre># 输出列表
                  [...,...,...]</pre>
                    </span></label>
                </div>
              </div>

              <!-- duchi 算法输入输出参数格式 -->
              <div v-if="showField('duchi_format')" id="duchi_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="duchi_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Duchi算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="duchi_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Duchi算法输出格式：<span>
                      <pre>{
                  # 输入值列表
                  "inputs": [...],
                  # 输出值列表
                  "outputs": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- pm 算法输入输出参数格式 -->
              <div v-if="showField('pm_format')" id="pm_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="pm_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PM算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="pm_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PM算法输出格式：<span>
                      <pre>{
                  # 输入值列表
                  "inputs": [...],
                  # 输出值列表
                  "outputs": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- laplace 算法输入输出参数格式 -->
              <div v-if="showField('laplace_format')" id="laplace_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="laplace_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Laplace算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="laplace_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Laplace算法输出格式：<span>
                      <pre>{
                  # 输入值列表
                  "inputs": [...],
                  # 输出值列表
                  "outputs": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- rr 算法输入输出参数格式 -->
              <div v-if="showField('rr_format')" id="rr_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="rr_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">RR算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="rr_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">RR算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- sue 算法输入输出参数格式 -->
              <div v-if="showField('sue_format')" id="sue_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="sue_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">SUE算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="sue_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">SUE算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- oue 算法输入输出参数格式 -->
              <div v-if="showField('oue_format')" id="oue_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="oue_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OUE算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="oue_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OUE算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- blh 算法输入输出参数格式 -->
              <div v-if="showField('blh_format')" id="blh_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="blh_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">BLH算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="blh_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">BLH算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- olh 算法输入输出参数格式 -->
              <div v-if="showField('olh_format')" id="olh_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="olh_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OLH算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="olh_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OLH算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- he 算法输入输出参数格式 -->
              <div v-if="showField('he_format')" id="he_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="he_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">HE算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="he_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">HE算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- K-subset 算法输入输出参数格式 -->
              <div v-if="showField('ksubset_format')" id="ksubset_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="ksubset_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">k-Subset算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="ksubset_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">k-Subset算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- privKVM 算法输入输出参数格式 -->
              <div v-if="showField('privKVM_format')" id="privKVM_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="privKVM_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PrivKVM算法输入参数格式：<span>键的数量, 迭代次数, 隐私预算, 输入数据</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="privKVM_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PrivKVM算法输出格式：<span>
                      <pre>{
                  # 索引值列表
                  "index_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- pckvUE 算法输入输出参数格式 -->
              <div v-if="showField('pckvUE_format')" id="pckvUE_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="pckvUE_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PCKV-UE算法输入参数格式：<span>键域大小, 填充长度, 键1离散概率, 键0离散概率, 值的扰动概率,
                      输入数据</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="pckvUE_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PCKV-UE算法输出格式：<span>
                      <pre>{
                  # 抽样值列表
                  "sample_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- pckvRR 算法输入输出参数格式 -->
              <div v-if="showField('pckvGRR_format')" id="pckvGRR_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="pckvGRR_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PCKV-GRR算法输入参数格式：<span>键域大小, 填充长度, 键1离散概率, 键0离散概率, 值的扰动概率,
                      输入数据</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="pckvGRR_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PCKV-GRR算法输出格式：<span>
                      <pre>{
                  # 抽样值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- dPAPPOR 算法输入输出参数格式 -->
              <div v-if="showField('dPAPPOR_format')" id="dPAPPOR_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="dPAPPOR_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">d-PAPPOR算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="dPAPPOR_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">d-PAPPOR算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- OLHSampling 算法输入输出参数格式 -->
              <div v-if="showField('OLHSampling_format')" id="OLHSampling_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="OLHSampling_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OLHSampling算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="OLHSampling_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OLHSampling算法输出格式：<span>
                      <pre>
                  {
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- OUESampling 算法输入输出参数格式 -->
              <div v-if="showField('OUESampling_format')" id="OUESampling_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="OUESampling_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OUESampling算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="OUESampling_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">OUESampling算法输出格式：<span>
                      <pre>
                  {
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- privSet 算法输入输出参数格式 -->
              <div v-if="showField('privSet_format')" id="privSet_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="privSet_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PrivSet算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="privSet_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">PrivSet算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- wheel 算法输入输出参数格式 -->
              <div v-if="showField('wheel_format')" id="wheel_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="wheel_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Wheel算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="wheel_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">Wheel算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>

              <!-- ldpMinner 算法输入输出参数格式 -->
              <div v-if="showField('ldpMinner_format')" id="ldpMinner_format" class="mb-2">
                <div class="d-flex align-items-center">
                  <label for="ldpMinner_format_input" class="form-label text-muted mb-2"
                    style="white-space: nowrap">ldpMinner算法输入参数格式：<span>隐私预算, 输入域, 数据, 测试输入数量</span></label>
                </div>
                <div class="d-flex align-items-center">
                  <label for="ldpMinner_format_output" class="form-label text-muted mb-2"
                    style="white-space: nowrap">LdpMinner算法输出格式：<span>
                      <pre>{
                  # 编码值列表
                  "encode_list": [...],
                  # 扰动值列表
                  "perturb_list": [...]
}</pre>
                    </span></label>
                </div>
              </div>


              <div class="d-flex align-items-center mb-2">
                <div v-if="formData.epsilon.show" id="epsilon" class="d-flex align-items-center me-3">
                  <label class="form-label mb-2 text-muted" style="white-space: nowrap">预设隐私预算：</label>
                  <el-input type="number" name="epsilon" v-model="formData.epsilon.content" min="0" step="0.01"
                    class="form-control ms-2" required="true" style="width: 120px" />
                </div>
                <div v-if="formData.accuracy.show" id="accuracy" class="d-flex align-items-center me-3">
                  <label class="form-label mb-2 text-muted" style="white-space: nowrap">测试精度 0~1.0</label>
                  <el-input type="number" name="accuracy" v-model="formData.accuracy.content" min="0" max="1.0"
                    step="0.01" class="form-control ms-2" required="true" style="width: 120px" />
                </div>
                <div v-if="formData.whole_n.show" id="whole_n" class="d-flex align-items-center">
                  <label class="form-label mb-2 text-muted" style="white-space: nowrap">测试输入数量：</label>
                  <el-input type="number" name="whole_n" v-model="formData.whole_n.content" min="0" step="1"
                    class="form-control ms-2" required="true" style="width: 120px" />
                </div>
              </div>

              <div class="d-flex align-items-center mb-2">
                <div v-if="formData.once_n.show" id="once_n" class="d-flex align-items-center">
                  <label class="form-label mb-2 text-muted" style="white-space: nowrap">单个输入运行次数：</label>
                  <el-input type="number" name="once_n" v-model="formData.once_n.content" min="0" step="1"
                    class="form-control ms-2" required="true" style="width: 120px" />
                </div>
              </div>

            </div>
          </el-form-item>
        </FormField>
      </div>

      <el-form-item class="mt-4">
        <el-button type="primary" native-type="submit">提交</el-button>
      </el-form-item>
    </el-card>
  </el-form>

  <el-dialog v-model="isProcessing" title="处理中" width="30%" :close-on-click-modal="false" :close-on-press-escape="false"
    :show-close="false">
    <div class="processing-content">
      <el-progress type="circle" :percentage="processingPercentage" />
      <p>{{ processingMessage }}</p>
    </div>
  </el-dialog>
</template>

<script setup>
import FormField from './FormField.vue';
import { ElForm, ElFormItem, ElCard, ElRadioGroup, ElRadioButton, ElButton, ElDialog, ElProgress } from 'element-plus';
import router from '@/router';
import { onMounted, reactive, ref, watch } from 'vue';
import { submitFormData } from '@/api/formSubmission';
import { useResultStore } from '@/stores/result';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  },
  currentForm: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['showContent']);

const selectedMethod = ref("code_");
const resultStore = useResultStore();

const isProcessing = ref(false);
const processingPercentage = ref(0);
const processingMessage = ref('正在提交数据...');

const selectedFile = ref(null);

// 添加对 currentForm 的 watch
watch(
  () => props.formData.alg_name.content,
  () => {
    // 当 currentForm 改变时，重置 selectedMethod 为默认值 "code_"
    selectedMethod.value = "code_";
  }
);

const showField = (fieldName) => {
  return props.formData[fieldName].show;
};

const changeMethod = (select) => {
  emit("showContent", select)
}

const submitForm = async () => {
  try {
    isProcessing.value = true;
    processingPercentage.value = 0;
    processingMessage.value = '正在提交数据...';


    console.log("此时的formData", props.formData);

    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (processingPercentage.value < 90) {
        processingPercentage.value += 10;
      }
    }, 1000);

    const result = await submitFormData(props.formData);

    clearInterval(progressInterval);
    processingPercentage.value = 100;
    processingMessage.value = '处理完成!';

    console.log("这里的reuslt", result)
    // resultStore.setResult(result);
    resultStore.setId(result.id)
    resultStore.setResult(result.result)
    resultStore.setEpsilon(result.epsilon)
    resultStore.setInputsN(result.inputs_n)
    resultStore.setInputKindsN(result.input_kinds_n)
    resultStore.setInputs(result.inputs)
    resultStore.setOutputs(result.outputs)
    console.log("这里的reuslt", result)
    // 短暂延迟后关闭模态框并跳转
    setTimeout(() => {
      isProcessing.value = false;
      router.push({ name: 'result' });
    }, 1000);

  } catch (error) {
    console.error(error);
    processingMessage.value = '提交代码出错，请重试';
    // 这里可以添加更多错误处理逻辑
    setTimeout(() => {
      isProcessing.value = false;
    }, 2000); // 延迟 3 秒后执行
  }
};

const handleFileChange = (file) => {
  console.log("上传的文件", file)
  // selectedFile.value = file.raw;
  props.formData['exe_file'].content = file.raw;
}

const inputTypeOptions = [
  { value: 'single_discrete_input', label: '离散' },
  { value: 'single_continuous_input', label: '连续' },
  // { value: 'discrete_set_input', label: '离散集合' },
  // { value: 'key_value_input', label: '键-值' }
];

const outputTypeOptions = [
  { value: 'single_discrete_output', label: '单个离散' },
  { value: 'single_continuous_output', label: '单个连续' },
  { value: 'multi_discrete_output', label: '多个离散' },
  { value: 'multi_continuous_output', label: '多个连续' },
  // { value: 'discrete_set_output', label: '离散集合' },
  // { value: 'key_value_output', label: '键-值' }
];

// const formOutputData = reactive({
//   output_type: {
//     content: outputTypeOptions[0].value
//   }
// });
onMounted(() => {
  // formOutputData.output_type.content = outputTypeOptions[0].value; // 设置为第一个选项的值
  props.formData['output_type'].content = outputTypeOptions[0].value; // 设置为第一个选项的值
});

const callMethods = [
  { value: 'code_', label: '代码调用' },
  { value: 'exe_', label: '可执行文件调用' },
  // { value: 'api_', label: '远程 api 调用' }
];

</script>

<style scoped>
.main-content {
  margin: 0 auto;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  width: 100%;
  max-height: 100vh;
  /* 添加最大高度 */
  overflow-y: auto;
  /* 添加垂直滚动 */
}

.algorithm-card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  overflow: hidden;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.algorithm-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 1rem;
  border-bottom: 2px solid #eaeaea;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 0.5rem;
  color: #409EFF;
}

.el-form-item {
  margin-bottom: 1.5rem;
}

.el-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.input-range {
  display: flex;
  align-items: center;
}

.range-separator {
  margin: 0 1rem;
  color: #909399;
}

.el-button {
  padding: 12px 20px;
  font-size: 1rem;
}

.call-method-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.el-radio-group {
  margin-bottom: 1rem;
}

.align-items-center {
  align-items: center;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.text-muted {
  color: #6c757d;
}

pre {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.875rem;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.command-line-info,
.output-format-info {
  margin-bottom: 0.5rem;
}

.command-line-info label,
.output-format-info label {
  display: block;
  white-space: normal;
}

.content {
  width: 100%;
}
</style>