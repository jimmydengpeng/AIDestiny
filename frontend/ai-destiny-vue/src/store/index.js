import { createStore } from 'vuex'

export default createStore({
  state: {
    // 用户信息
    userInfo: null,
    // 八字算命结果
    fortuneResult: null,
    // 主题设置
    theme: {
      primaryColor: '#7b68ee',
      secondaryColor: '#9370db',
      accentColor: '#ff6b6b'
    }
  },
  getters: {
    // 获取用户信息
    getUserInfo: state => state.userInfo,
    // 获取算命结果
    getFortuneResult: state => state.fortuneResult,
    // 获取主题设置
    getTheme: state => state.theme
  },
  mutations: {
    // 设置用户信息
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
    },
    // 设置算命结果
    SET_FORTUNE_RESULT(state, result) {
      state.fortuneResult = result
    },
    // 清除算命结果
    CLEAR_FORTUNE_RESULT(state) {
      state.fortuneResult = null
    }
  },
  actions: {
    // 保存用户信息
    saveUserInfo({ commit }, userInfo) {
      commit('SET_USER_INFO', userInfo)
    },
    // 保存算命结果
    saveFortuneResult({ commit }, result) {
      commit('SET_FORTUNE_RESULT', result)
    },
    // 清除算命结果
    clearFortuneResult({ commit }) {
      commit('CLEAR_FORTUNE_RESULT')
    }
  },
  modules: {
    // 可以在这里添加模块化的状态
  }
}) 