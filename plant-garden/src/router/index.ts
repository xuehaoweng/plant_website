import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/plants',
    name: 'plants',
    component: () => import('../views/Plants.vue'),
    meta: {
      title: '植物分类'
    }
  },
  {
    path: '/care-guides',
    name: 'care-guides',
    component: () => import('../views/CareGuides.vue'),
    meta: {
      title: '养护指南'
    }
  },
  {
    path: '/problems',
    name: 'problems',
    component: () => import('../views/ProblemsView.vue'),
    meta: {
      title: '常见问题'
    }
  },
  {
    path: '/community',
    name: 'community',
    component: () => import('../views/CommunityView.vue'),
    meta: {
      title: '社区交流'
    }
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('../views/UserView.vue'),
    meta: {
      title: '个人中心',
      requiresAuth: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: {
      title: '页面未找到'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - 绿居园艺`

  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      next({ name: 'home', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router 