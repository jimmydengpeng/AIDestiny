<template>
  <section class="fortune-form glass-card">
    <h3>填写您的出生信息</h3>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="birthDate">出生日期</label>
        <input 
          type="date" 
          id="birthDate" 
          v-model="formData.birthDate" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="birthTime">出生时间</label>
        <input 
          type="time" 
          id="birthTime" 
          v-model="formData.birthTime" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="gender">性别</label>
        <div class="radio-group">
          <label class="radio-label">
            <input 
              type="radio" 
              name="gender" 
              value="male" 
              v-model="formData.gender"
            >
            <span class="radio-custom"></span>
            男
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              name="gender" 
              value="female" 
              v-model="formData.gender"
            >
            <span class="radio-custom"></span>
            女
          </label>
        </div>
      </div>
      
      <div class="form-group">
        <label for="birthPlace">出生地点</label>
        <input 
          type="text" 
          id="birthPlace" 
          v-model="formData.birthPlace" 
          placeholder="例如：北京市" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="analysisType">分析类型</label>
        <select id="analysisType" v-model="formData.analysisType">
          <option 
            v-for="option in analysisOptions" 
            :key="option.value" 
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>
      
      <button type="submit" class="btn primary-btn">开始分析</button>
    </form>
  </section>
</template>

<script>
export default {
  name: 'FortuneForm',
  data() {
    return {
      formData: {
        birthDate: '',
        birthTime: '',
        gender: 'male',
        birthPlace: '',
        analysisType: 'comprehensive'
      },
      analysisOptions: [
        { value: 'comprehensive', label: '综合分析' },
        { value: 'personality', label: '性格特质' },
        { value: 'career', label: '事业财运' },
        { value: 'relationship', label: '感情婚姻' },
        { value: 'health', label: '健康状况' }
      ]
    }
  },
  methods: {
    submitForm() {
      // 创建一个合并的日期时间对象
      const birthDateTime = new Date(`${this.formData.birthDate}T${this.formData.birthTime}`)
      
      // 创建提交的数据对象
      const submitData = {
        ...this.formData,
        birthDateTime
      }
      
      // 触发提交事件，将数据传递给父组件
      this.$emit('form-submitted', submitData)
    }
  }
}
</script>

<style scoped>
.fortune-form {
  padding: 30px;
  margin-bottom: 30px;
}

.fortune-form h3 {
  text-align: center;
  margin-bottom: 25px;
  color: var(--primary-color);
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-color);
}

.form-group input[type="date"],
.form-group input[type="time"],
.form-group input[type="text"],
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.8);
  font-family: inherit;
  font-size: 1rem;
  transition: var(--transition);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(123, 104, 238, 0.2);
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: normal;
}

.radio-label input[type="radio"] {
  position: absolute;
  opacity: 0;
}

.radio-custom {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--primary-color);
  margin-right: 8px;
  position: relative;
  transition: var(--transition);
}

.radio-label input[type="radio"]:checked + .radio-custom:after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--primary-color);
}

.radio-label:hover .radio-custom {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 2px rgba(123, 104, 238, 0.2);
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 15px center;
  background-size: 15px;
}

@media (max-width: 768px) {
  .fortune-form {
    padding: 20px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 10px;
  }
}
</style> 