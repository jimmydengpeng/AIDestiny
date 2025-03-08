# AI命运占卜应用 - Vue版本

## 技术栈

- **前端框架**: Vue 3.3.4
- **构建工具**: Vite 4.4.9
- **状态管理**: Vuex 4.1.0
- **路由管理**: Vue Router 4.2.4
- **HTTP 客户端**: Axios 1.8.1
- **开发工具**:
  - @vitejs/plugin-vue: Vue 3 单文件组件支持
  - @vue/compiler-sfc: Vue 3 单文件组件编译器

## 项目特点

- 使用 Vue 3 Composition API
- 基于 Vite 的现代构建工具链
- 模块化的状态管理
- 路由系统支持

## 开发环境要求

- Node.js (推荐 16.0.0 或更高版本)
- npm 或 yarn 包管理器

## 安装步骤

1. 克隆项目到本地：
```bash
git clone <项目地址>
cd ai-destiny-vue
```

2. 安装依赖：
```bash
# 使用 npm
npm install

# 或使用 yarn
yarn install
```

3. 启动开发服务器：
```bash
# 使用 npm
npm run dev

# 或使用 yarn
yarn dev
```

4. 构建生产版本：
```bash
# 使用 npm
npm run build

# 或使用 yarn
yarn build
```

## 项目结构

```
ai-destiny-vue/
├── src/              # 源代码目录
├── public/           # 静态资源目录
├── index.html        # HTML 入口文件
├── vite.config.js    # Vite 配置文件
├── package.json      # 项目依赖配置
└── README.md         # 项目说明文档
```

## 开发注意事项

1. 本项目使用 Vue 3 和 Composition API，请确保熟悉相关概念
2. 使用 Vite 作为开发和构建工具，支持热模块替换（HMR）
3. 项目使用 ESM 模块系统，配置类型为 "type": "module"

## 相关命令

- `npm run dev`: 启动开发服务器
- `npm run build`: 构建生产版本
- `npm run preview`: 本地预览生产构建 