import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutView.vue'
import QueryView from '../views/QueryView.vue'
import LLMView from '../views/LLMView.vue'
import VectorDbView from '../views/VectorDbView.vue'

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
    {
      path: '/vector_db/',
      name: 'vector_db',
      component: VectorDbView
    },
  ]
})

export default router
