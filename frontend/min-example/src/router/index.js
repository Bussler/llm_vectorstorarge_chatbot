import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutView.vue'
import QueryView from '../views/QueryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/about/',
      name: 'about',
      component: AboutView
    },
    {
      path: '/',
      name: 'query',
      component: QueryView
    },
  ]
})

export default router
