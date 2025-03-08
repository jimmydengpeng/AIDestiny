<template>
  <div class="fortune container">
    <div class="glass-card">
      <h2>飞灵八字命盘</h2>
      <form @submit.prevent="submitForm" class="fortune-form">
        <div class="form-group">
          <label for="gender">性别</label>
          <div class="radio-group">
            <label class="radio-label">
              <input 
                type="radio" 
                v-model="formData.gender" 
                value="male"
                required
              >
              男
            </label>
            <label class="radio-label">
              <input 
                type="radio" 
                v-model="formData.gender" 
                value="female"
              >
              女
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="birthDate">出生日期时间</label>
          <input 
            type="datetime-local" 
            id="birthDate" 
            v-model="formData.birthDate"
            required
          >
        </div>

        <div class="form-group">
          <label for="calendar">历法选择</label>
          <div class="radio-group">
            <label class="radio-label">
              <input 
                type="radio" 
                v-model="formData.calendar" 
                value="solar"
                checked
              >
              公历
            </label>
            <label class="radio-label">
              <input 
                type="radio" 
                v-model="formData.calendar" 
                value="lunar"
              >
              农历
            </label>
          </div>
        </div>

        <!-- 添加状态显示 -->
        <div v-if="error" class="error-message">
          <p>{{ error }}</p>
        </div>
        
        <button 
          type="submit" 
          class="btn primary-btn"
          :disabled="loading"
        >
          {{ loading ? '计算中...' : '开始测算' }}
        </button>
        
        <!-- 添加调试信息 -->
        <div v-if="debugInfo" class="debug-info">
          <h4>调试信息</h4>
          <pre>{{ debugInfo }}</pre>
        </div>
      </form>

      <!-- 结果展示区域 -->
      <div v-if="result" class="result-section">
        <div class="result-card">
          <h3>八字命盘</h3>
          <p class="bazi-text">{{ result.bazi }}</p>
          
          <h3>命理解读</h3>
          <div class="reading-content" v-html="formatReading(result.reading)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const formData = ref({
  gender: 'male',
  birthDate: '',
  calendar: 'solar'
})

const loading = ref(false)
const result = ref(null)
const error = ref(null)
const debugInfo = ref(null)

const formatReading = (text) => {
  return text.replace(/\n/g, '<br>')
}

const submitForm = async () => {
  try {
    loading.value = true
    error.value = null
    debugInfo.value = null
    
    // 验证表单
    if (!formData.value.birthDate) {
      error.value = '请选择出生日期时间'
      return
    }
    
    const date = new Date(formData.value.birthDate)
    
    // 构建请求数据
    const requestData = {
      gender: formData.value.gender,
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes()
    }
    
    debugInfo.value = `请求数据: ${JSON.stringify(requestData, null, 2)}`
    console.log('发送请求数据:', requestData)
    
    // 发送请求到后端API
    const response = await axios.post('/api/basic_report', requestData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('收到响应:', response.data)
    debugInfo.value += `\n\n响应数据: ${JSON.stringify(response.data, null, 2)}`
    result.value = response.data
    
  } catch (err) {
    console.error('占卜出错:', err)
    error.value = err.response?.data?.detail || `请求失败: ${err.message}`
    debugInfo.value += `\n\n错误信息: ${JSON.stringify(err.response?.data || err.message, null, 2)}`
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fortune {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.fortune-form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 24px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

input[type="datetime-local"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input[type="datetime-local"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.result-section {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.result-card {
  text-align: left;
}

.bazi-text {
  font-size: 24px;
  color: #2c3e50;
  text-align: center;
  margin: 20px 0;
  font-weight: bold;
}

.reading-content {
  line-height: 1.8;
  color: #4a5568;
}

h2 {
  color: #2c3e50;
  margin-bottom: 30px;
}

h3 {
  color: #2c3e50;
  margin: 20px 0 15px;
}

.error-message {
  background-color: #fff5f5;
  color: #e53e3e;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 15px;
  text-align: left;
}

.debug-info {
  margin-top: 20px;
  text-align: left;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
  overflow-x: auto;
}

.debug-info pre {
  white-space: pre-wrap;
  word-break: break-all;
}

@media (max-width: 768px) {
  .fortune {
    padding: 20px 15px;
  }
  
  .glass-card {
    padding: 20px;
  }
}
</style> 