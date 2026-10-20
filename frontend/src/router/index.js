import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'login', component: () => import('../views/LoginRegister.vue') },
  {
    path: '/',
    name: 'chat',
    component: () => import('../views/Chat.vue'),
    meta: { requiresAuth: true },
  },
  {
    // 知识库管理：专属于管理员的功能模块，普通用户访问直接被拦截
    path: '/admin/kb',
    name: 'adminKb',
    component: () => import('../views/AdminKb.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫：登录态校验 + 管理员角色校验
router.beforeEach((to) => {
  const auth = JSON.parse(localStorage.getItem('auth') || '{}')
  if (to.meta.requiresAuth && !auth.token) return { path: '/login' }
  if (to.meta.requiresAdmin && auth.role !== 'admin') return { path: '/' }
  if (to.path === '/login' && auth.token) return { path: '/' }
})

export default router
