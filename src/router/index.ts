import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/index.vue'),
    },{
      path: '/register',
      name: 'register',
      component: () => import('../views/register.vue'),
    },{
      path: '/login',
      name: 'login',
      component: () => import('../views/login.vue'),
    }
  ]
})

export default router
