<template>
  <footer class="glass-card">
    <div class="footer-content">
      <div class="footer-logo">
        <i class="fas fa-moon"></i>
        <h3>AI命运占卜</h3>
      </div>
      <div class="footer-links">
        <h4>快速链接</h4>
        <ul>
          <li v-for="item in navItems" :key="item.path">
            <router-link :to="item.path">{{ item.name }}</router-link>
          </li>
        </ul>
      </div>
      <div class="footer-contact">
        <h4>联系我们</h4>
        <p><i class="fas fa-envelope"></i> contact@aidestiny.com</p>
        <div class="social-icons">
          <a href="#" v-for="(icon, index) in socialIcons" :key="index">
            <i :class="icon"></i>
          </a>
        </div>
      </div>
    </div>
    <div class="copyright">
      <p>&copy; {{ currentYear }} AI命运占卜. 保留所有权利.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      navItems: [
        { name: '首页', path: '/' },
        { name: '八字算命', path: '/fortune' },
        { name: '关于我们', path: '/about' }
      ],
      socialIcons: [
        'fab fa-weixin',
        'fab fa-weibo',
        'fab fa-qq'
      ]
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
footer {
  margin-top: 30px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.footer-logo {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.footer-logo i {
  font-size: 1.5rem;
  color: var(--primary-color);
  margin-right: 10px;
}

.footer-logo h3 {
  font-size: 1.2rem;
  color: var(--primary-color);
}

.footer-links, .footer-contact {
  margin-bottom: 15px;
}

.footer-links h4, .footer-contact h4 {
  margin-bottom: 10px;
  color: var(--primary-color);
}

.footer-links ul {
  list-style: none;
}

.footer-links ul li {
  margin-bottom: 8px;
}

.footer-links ul li a {
  color: var(--text-color);
  text-decoration: none;
  transition: var(--transition);
}

.footer-links ul li a:hover {
  color: var(--primary-color);
}

.footer-contact p {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.footer-contact p i {
  margin-right: 10px;
  color: var(--primary-color);
}

.social-icons {
  display: flex;
  margin-top: 15px;
}

.social-icons a {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  margin-right: 10px;
  color: var(--primary-color);
  transition: var(--transition);
}

.social-icons a:hover {
  background: var(--primary-color);
  color: var(--light-text);
  transform: translateY(-3px);
}

.copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
  }
}
</style> 