<template>
  <div class="about container">
    <div class="glass-card">
      <h2>关于飞灵</h2>
      <p>飞灵(Fatelling)是一个专注于八字算命的智能应用。我们结合传统命理学和现代技术，致力于为用户提供科学、准确、个性化的八字命盘解读服务。</p>
      <div class="features">
        <div class="feature">
          <h3>智能解读</h3>
          <p>采用先进的智能算法，提供精准的八字命盘分析。</p>
        </div>
        <div class="feature">
          <h3>传统命理</h3>
          <p>融合传统八字命理学的精髓，传承千年智慧。</p>
        </div>
        <div class="feature">
          <h3>个性化服务</h3>
          <p>根据个人八字命盘，提供量身定制的命理建议。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 组件逻辑
</script>

<style scoped>
.about {
  width: 100%;
  padding: 40px 0;
}

h2 {
  color: var(--primary-color);
  margin-bottom: 20px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.feature {
  padding: 20px;
  text-align: left;
}

.feature h3 {
  color: var(--secondary-color);
  margin-bottom: 10px;
}

.feature p {
  color: var(--text-color);
  line-height: 1.6;
}
</style> 