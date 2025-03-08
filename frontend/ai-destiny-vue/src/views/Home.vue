<template>
  <div class="home">
    <div class="hero">
      <h1>飞灵</h1>
      <p class="subtitle">专业八字算命，智能解读人生</p>
    </div>
    
    <div class="features">
      <div class="feature-card" @click="$router.push('/fortune')">
        <h3>八字命盘</h3>
        <p>基于出生年月日时的精准八字分析</p>
        <button class="primary-btn">开始测算</button>
      </div>
      
      <div class="feature-card">
        <h3>命理解读</h3>
        <p>智能分析命盘，深入解读人生</p>
        <button class="primary-btn">即将推出</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 组件逻辑
</script>

<style scoped>
.home {
  width: 100%;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
  margin-bottom: 40px;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
  color: white;
}

.subtitle {
  font-size: 1.2em;
  opacity: 0.9;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  padding: 20px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-card p {
  color: #666;
  margin-bottom: 20px;
}

.primary-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.primary-btn:hover {
  background: #764ba2;
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
}
</style> 