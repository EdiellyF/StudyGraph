<template>
  <section class="max-w-4xl mx-auto">
    <!-- Search Bar -->
    <div class="mb-6">
      <div class="bg-white rounded-2xl shadow-sm p-6">
        <div class="flex gap-4">
          <input
            v-model="searchQuery"
            @keyup.enter="performSearch"
            type="text"
            placeholder="Procure por usuários, cursos ou instituições..."
            class="flex-1 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine"
          />
          <button
            @click="performSearch"
            :disabled="loading"
            class="px-6 py-3 rounded-full bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50"
          >
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="loading" class="text-center py-12 text-slate-500">
      <p>Carregando resultados...</p>
    </div>

    <div v-else-if="searchPerformed && results.length === 0" class="bg-white rounded-2xl shadow-sm p-12 text-center">
      <p class="text-slate-500 mb-4">Nenhum resultado encontrado.</p>
      <p class="text-slate-400 text-sm">Tente buscar por outro termo.</p>
    </div>

    <div v-else-if="results.length > 0" class="space-y-4">
      <div
        v-for="user in results"
        :key="user.id"
        class="bg-white rounded-2xl shadow-sm p-6"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <div class="w-16 h-16 rounded-full bg-malva flex items-center justify-center text-white text-xl flex-shrink-0">
              {{ user.name?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="flex-1 min-w-0">
              <router-link
                :to="`/profile/${user.id}`"
                class="text-lg font-semibold text-wine hover:underline"
              >
                {{ user.name }}
              </router-link>
              <p class="text-slate-600 text-sm">{{ user.institution }}</p>
              <p class="text-slate-500 text-sm">{{ user.course }}</p>
              <p class="text-slate-400 text-xs mt-1">{{ user.followersCount }} seguidores</p>
            </div>
          </div>
          <button
            @click="followUser(user.id)"
            class="px-6 py-2 rounded-full border border-wine text-wine hover:bg-wine hover:text-white transition whitespace-nowrap"
          >
            Seguir
          </button>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-2xl shadow-sm p-12 text-center">
      <p class="text-slate-500 mb-4">Comece a explorar</p>
      <p class="text-slate-400 text-sm">Use a barra de busca para encontrar usuários, cursos e instituições.</p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const searchQuery = ref('')
const results = ref([])
const loading = ref(false)
const searchPerformed = ref(false)

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function performSearch() {
  if (!searchQuery.value.trim()) return
  
  loading.value = true
  searchPerformed.value = true
  
  try {
    const response = await fetch(
      `${API_BASE}/users/search?q=${encodeURIComponent(searchQuery.value)}`,
      {
        headers: { Authorization: `Bearer ${auth.token}` },
      }
    )
    
    if (response.ok) {
      results.value = await response.json()
    }
  } catch (error) {
    console.error('Error searching users:', error)
  } finally {
    loading.value = false
  }
}

async function followUser(userId) {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}/follow`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    if (response.ok) {
      // Remove user from results
      results.value = results.value.filter(u => u.id !== userId)
    }
  } catch (error) {
    console.error('Error following user:', error)
  }
}
</script>
