import { createRouter, createWebHistory } from 'vue-router'
// @ts-ignore
import MainPage from '@/views/MainPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainPage
    },
    {
      path: '/publishData',
      name: 'publishData',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
// @ts-ignore

      component: () => import('../views/PublishData.vue')
    },
    {
      path: "/publishDataResult",
      name: "publishDataResult",
// @ts-ignore

      component: () => import('../views/PublishDataResult.vue')
    },
    {
      path: "/result",
      name: "result",
// @ts-ignore

      component: () => import('../views/Result.vue')
    }
  ]
})

export default router
