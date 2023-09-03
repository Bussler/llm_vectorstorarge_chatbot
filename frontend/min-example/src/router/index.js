import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutView.vue'
import QueryView from '../views/QueryView.vue'
import LLMView from '../views/LLMView.vue'

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
    {
      path: '/llm/',
      name: 'llm',
      component: LLMView
    },
  ]
})

export default router
