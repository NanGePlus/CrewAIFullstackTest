<template>
    <div class="crew-form-container">
      <el-form :model="form" label-width="80px" ref="crewForm" :rules="rules">
        <el-form-item label="网址" prop="customer_domain">
          <el-input v-model="form.customer_domain" placeholder="请输入网址"></el-input>
        </el-form-item>
        <el-form-item label="项目描述" prop="project_description">
          <el-input v-model="form.project_description" placeholder="请输入项目描述"></el-input>
        </el-form-item>
        <el-form-item label="富文本内容展示">
          <el-input type="textarea" v-model="richTextContent" :rows="6" :readonly="true"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit('start')" class="submit-button">启动</el-button>
          <el-button type="success" @click="handleSubmit('refresh')" class="refresh-button">刷新</el-button>
        </el-form-item>
      </el-form>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import axios from 'axios';
  
  // 表单数据
  const form = ref({
    customer_domain: '',
    project_description: ''
  });
  const richTextContent = ref('');
  const jobId = ref('');
  const crewForm = ref(null); // 使用 ref 获取 el-form 的引用
  
  // 验证规则
  const rules = computed(() => ({
    customer_domain: [
      { required: true, message: '请输入网址', trigger: 'blur' }
    ],
    project_description: [
      { required: true, message: '请输入项目描述', trigger: 'blur' }
    ]
  }));
  
  // 提交处理函数
  const handleSubmit = async (action) => {
    try {
      const isValid = await crewForm.value.validate(); // 正确调用 validate 方法
  
      if (isValid) {
        if (action === 'start') {
          // 发起启动按钮请求
          const response = await axios.post('http://127.0.0.1:8012/api/crew', {
            customer_domain: form.value.customer_domain,
            project_description: form.value.project_description
          });
          jobId.value = response.data.job_id; // 临时存储 job_id
        } else if (action === 'refresh') {
          // 发起刷新按钮请求
          const response = await axios.get(`http://127.0.0.1:8012/api/crew/${jobId.value}`);
          richTextContent.value = JSON.stringify(response.data); // 更新富文本内容展示
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  </script>
  
  <style scoped>
  .crew-form-container {
    width: 1000px; /* 容器宽度设置为1000px */
    margin: 20px auto; /* 居中容器 */
    padding: 20px; /* 内边距 */
    border-radius: 8px; /* 圆角 */
    background-color: #f9f9f9; /* 背景色 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  }
  
  .el-form-item {
    margin-bottom: 20px; /* 每个表单项底部间距 */
  }
  
  .submit-button,
  .refresh-button {
    margin-right: 10px; /* 按钮之间的间距 */
  }
  
  .submit-button {
    background-color: #409eff; /* 启动按钮颜色 */
    border-color: #409eff; /* 启动按钮边框颜色 */
  }
  
  .refresh-button {
    background-color: #67c23a; /* 刷新按钮颜色 */
    border-color: #67c23a; /* 刷新按钮边框颜色 */
  }
  
  .el-input {
    border-radius: 4px; /* 输入框圆角 */
  }
  
  .el-input[type='textarea'] {
    resize: none; /* 禁止调整文本区域大小 */
  }
  </style>
  