import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import FeedView from '../views/FeedView.vue'
import AppShell from '../components/AppShell.vue'

const routes = [
  {
    path: '/',
    component: AppShell,
    children: [
      { path: '', name: 'Home', component: HomeView },
      { path: 'feed', name: 'Feed', component: FeedView },
      { path: 'profile', name: 'Profile', component: ProfileView },
    ]
  },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
