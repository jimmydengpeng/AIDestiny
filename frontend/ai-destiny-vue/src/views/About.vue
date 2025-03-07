<template>
  <div class="about container">
    <div class="glass-card">
      <h2>关于我们</h2>
      <p>AI命运占卜系统是一个结合传统命理学和现代人工智能技术的创新应用。我们致力于为用户提供科学、准确、个性化的命运解读服务。</p>
      <div class="features">
        <div class="feature">
          <h3>AI 技术</h3>
          <p>采用先进的人工智能算法，提供精准的命运分析。</p>
        </div>
        <div class="feature">
          <h3>传统智慧</h3>
          <p>融合传统命理学的精髓，传承千年智慧。</p>
        </div>
        <div class="feature">
          <h3>个性化服务</h3>
          <p>根据个人具体情况，提供量身定制的建议。</p>
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