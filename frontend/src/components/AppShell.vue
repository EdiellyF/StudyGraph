<template>
  <div class="min-h-screen bg-cream flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-wine text-white flex flex-col fixed h-full">
      <div class="p-6">
        <router-link to="/feed" class="font-bold text-2xl">StudyGraph</router-link>
      </div>
      
      <nav class="flex-1 px-4">
        <ul class="space-y-2">
          <li>
            <router-link 
              to="/feed" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition"
              active-class="bg-white/20"
            >
              <span>📰</span>
              <span>Feed</span>
            </router-link>
          </li>
          <li>
            <router-link 
              to="/explore" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition"
              active-class="bg-white/20"
            >
              <span>🔍</span>
              <span>Explorar</span>
            </router-link>
          </li>
          <li>
            <router-link 
              to="/notifications" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition"
              active-class="bg-white/20"
            >
              <span>🔔</span>
              <span>Notificações</span>
            </router-link>
          </li>
          <li>
            <router-link 
              to="/saved" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition"
              active-class="bg-white/20"
            >
              <span>🔖</span>
              <span>Salvos</span>
            </router-link>
          </li>
          <li>
            <router-link 
              to="/settings" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition"
              active-class="bg-white/20"
            >
              <span>⚙️</span>
              <span>Ajustes</span>
            </router-link>
          </li>
        </ul>
      </nav>

      <div class="p-4 border-t border-white/10">
        <div v-if="isAuthenticated" class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-malva flex items-center justify-center">
            {{ auth.user?.name?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div class="flex-1">
            <p class="font-medium text-sm truncate">{{ auth.user?.name }}</p>
            <p class="text-xs text-rose opacity-80">@{{ auth.user?.name?.toLowerCase().replace(/\s/g, '') }}</p>
          </div>
        </div>
        <button 
          v-if="isAuthenticated"
          @click="logout" 
          class="w-full px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 transition text-sm"
        >
          Sair
        </button>
        <router-link 
          v-else 
          to="/login" 
          class="block w-full px-4 py-2 rounded-xl bg-malva hover:bg-opacity-90 transition text-sm text-center"
        >
          Entrar
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 ml-64">
      <!-- TopBar -->
      <header class="bg-white shadow-sm sticky top-0 z-10">
        <div class="px-6 py-4 flex items-center justify-between">
          <div class="flex-1 max-w-xl">
            <input 
              type="text" 
              placeholder="Buscar posts, pessoas ou cursos..." 
              class="w-full px-4 py-2 rounded-full border border-slate-200 focus:outline-none focus:ring-2 focus:ring-malva"
            />
          </div>
          <div class="flex items-center gap-4 ml-4">
            <button class="p-2 rounded-full hover:bg-slate-100 transition relative">
              🔔
              <span class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <router-link 
              v-if="isAuthenticated" 
              to="/profile" 
              class="w-10 h-10 rounded-full bg-wine flex items-center justify-center text-white hover:bg-opacity-90 transition"
            >
              {{ auth.user?.name?.charAt(0).toUpperCase() || 'U' }}
            </router-link>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const isAuthenticated = computed(() => auth.isAuthenticated)

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
