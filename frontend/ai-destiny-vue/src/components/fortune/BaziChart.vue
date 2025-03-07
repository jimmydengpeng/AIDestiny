<template>
  <div class="bazi-chart">
    <div class="chart-title">八字命盘</div>
    <div class="chart-grid">
      <div 
        v-for="(pillar, index) in pillars" 
        :key="index" 
        class="chart-cell"
      >
        <div class="cell-title">{{ pillar.title }}</div>
        <div class="cell-content">
          <div class="heavenly-stem">{{ pillar.stem }}</div>
          <div class="earthly-branch">{{ pillar.branch }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaziChart',
  props: {
    pillars: {
      type: Array,
      required: true,
      // 默认值为空的四柱
      default: () => [
        { title: '年柱', stem: '', branch: '' },
        { title: '月柱', stem: '', branch: '' },
        { title: '日柱', stem: '', branch: '' },
        { title: '时柱', stem: '', branch: '' }
      ]
    }
  }
}
</script>

<style scoped>
.bazi-chart {
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.chart-title {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.chart-cell {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  transition: var(--transition);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.chart-cell:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.cell-title {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 10px;
  color: var(--text-color);
}

.cell-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.heavenly-stem, .earthly-branch {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  font-weight: 600;
  font-size: 1.2rem;
}

.heavenly-stem {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--light-text);
  margin-bottom: 5px;
}

.earthly-branch {
  background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
  color: var(--light-text);
}

@media (max-width: 768px) {
  .chart-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .chart-grid {
    grid-template-columns: 1fr;
  }
}
</style> 