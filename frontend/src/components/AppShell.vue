<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-slate-900 text-slate-100 px-6 py-4 shadow-md">
      <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
        <router-link to="/" class="font-bold text-lg">StudyGraph</router-link>
        <nav class="flex gap-3">
          <router-link to="/" class="text-slate-200 hover:text-white">Home</router-link>
          <router-link to="/profile" class="text-slate-200 hover:text-white">Perfil</router-link>
          <router-link v-if="!isAuthenticated" to="/login" class="text-slate-200 hover:text-white">Login</router-link>
          <router-link v-if="!isAuthenticated" to="/register" class="text-slate-200 hover:text-white">Cadastro</router-link>
          <button v-if="isAuthenticated" @click="logout" class="text-slate-200 hover:text-white">Sair</button>
        </nav>
      </div>
    </header>

    <div class="flex-1 bg-slate-100">
      <main class="max-w-7xl mx-auto px-6 py-8">
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
