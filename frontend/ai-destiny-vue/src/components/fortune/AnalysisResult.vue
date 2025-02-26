<template>
  <div class="analysis-result">
    <div class="result-section-title">
      <i :class="icon"></i>
      <h4>{{ title }}</h4>
    </div>
    <div class="result-content">
      <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
        <p>AI正在分析...</p>
      </div>
      <div v-else>
        <p v-for="(paragraph, index) in contentArray" :key="index">
          {{ paragraph }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnalysisResult',
  props: {
    icon: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    content: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    contentArray() {
      // 将内容拆分为段落数组
      if (!this.content) return []
      return this.content.split('\n').filter(p => p.trim() !== '')
    }
  }
}
</script>

<style scoped>
.analysis-result {
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 20px;
  transition: var(--transition);
}

.analysis-result:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.result-section-title {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.result-section-title i {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--light-text);
  margin-right: 10px;
  font-size: 0.9rem;
}

.result-section-title h4 {
  font-size: 1.1rem;
  color: var(--primary-color);
}

.result-content {
  padding: 0 10px;
}

.result-content p {
  margin-bottom: 15px;
  line-height: 1.6;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(123, 104, 238, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 