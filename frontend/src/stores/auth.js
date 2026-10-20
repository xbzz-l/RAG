import { defineStore } from 'pinia'

/**
 * 登录状态：token/username/role，持久化到 localStorage
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '',
    username: '',
    role: '',
  }),
  getters: {
    isLoggedIn: (s) => !!s.token,
    isAdmin: (s) => s.role === 'admin',
  },
  actions: {
    /** 登录/注册成功后写入状态 */
    setAuth({ access_token, username, role }) {
      this.token = access_token
      this.username = username
      this.role = role
      localStorage.setItem('auth', JSON.stringify({ token: access_token, username, role }))
    },
    /** 刷新页面时从 localStorage 恢复状态 */
    restore() {
      const saved = JSON.parse(localStorage.getItem('auth') || '{}')
      if (saved.token) {
        this.token = saved.token
        this.username = saved.username
        this.role = saved.role
      }
    },
    logout() {
      this.token = ''
      this.username = ''
      this.role = ''
      localStorage.removeItem('auth')
    },
  },
})
