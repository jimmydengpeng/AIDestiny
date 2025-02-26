<template>
  <header class="glass-card">
    <div class="logo">
      <i class="fas fa-moon"></i>
      <h1>AI命运占卜</h1>
    </div>
    <nav>
      <ul>
        <li v-for="item in navItems" :key="item.path">
          <router-link :to="item.path" :class="{ active: isActive(item.path) }">
            {{ item.name }}
          </router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      navItems: [
        { name: '首页', path: '/' },
        { name: '八字算命', path: '/fortune' },
        { name: '关于我们', path: '/about' }
      ]
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path
    }
  }
}
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo i {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin-right: 10px;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

nav ul {
  display: flex;
  list-style: none;
}

nav ul li {
  margin-left: 20px;
}

nav ul li a {
  color: var(--text-color);
  text-decoration: none;
  font-weight: 500;
  position: relative;
  padding-bottom: 5px;
}

nav ul li a:hover, nav ul li a.active {
  color: var(--primary-color);
}

nav ul li a:after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: var(--primary-color);
  transition: var(--transition);
}

nav ul li a:hover:after, nav ul li a.active:after {
  width: 100%;
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
  }
  
  nav ul {
    margin-top: 15px;
  }
  
  nav ul li {
    margin: 0 10px;
  }
}

@media (max-width: 480px) {
  header {
    padding: 15px;
  }
  
  nav ul {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  nav ul li {
    margin: 5px 10px;
  }
}
</style> 