import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './styles/global.css'

// 创建Vue应用实例
const app = createApp(App)

// 使用路由和状态管理
app.use(router)
app.use(store)

// 挂载应用
app.mount('#app') 