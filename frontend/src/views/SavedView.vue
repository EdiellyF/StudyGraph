<template>
  <section class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-wine">Posts Salvos</h1>
      <p class="text-slate-600 mt-2">Seus posts favoritos em um só lugar</p>
    </div>

    <div v-if="loading" class="text-center py-12 text-slate-500">
      <p>Carregando posts salvos...</p>
    </div>

    <div v-else-if="savedPosts.length === 0" class="bg-white rounded-2xl shadow-sm p-12 text-center">
      <p class="text-slate-500 mb-4">Você ainda não salvou nenhum post.</p>
      <p class="text-slate-400 text-sm">Clique no ícone de bookmark para salvar seus posts favoritos.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="post in savedPosts"
        :key="post.id"
        class="bg-white rounded-2xl shadow-sm p-6"
      >
        <div class="flex gap-4">
          <div class="w-12 h-12 rounded-full bg-wine flex items-center justify-center text-white flex-shrink-0">
            {{ post.authorName?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <router-link
                :to="`/profile/${post.authorId}`"
                class="font-semibold text-wine hover:underline"
              >
                {{ post.authorName }}
              </router-link>
              <span class="text-slate-400 text-sm">·</span>
              <span class="text-slate-400 text-sm">{{ formatDate(post.createdAt) }}</span>
            </div>
            <p class="text-slate-700 whitespace-pre-wrap mb-4">{{ post.content }}</p>
            <div v-if="post.images && post.images.length > 0" class="grid gap-2 mb-4" :class="post.images.length === 1 ? 'grid-cols-1' : 'grid-cols-2'">
              <img
                v-for="(img, idx) in post.images"
                :key="idx"
                :src="img"
                class="rounded-lg w-full h-auto object-cover max-h-96"
                alt="Post image"
              />
            </div>
            <div class="flex items-center gap-6 text-slate-500">
              <button
                @click="toggleLike(post.id)"
                :class="[
                  'flex items-center gap-2 transition',
                  likedPosts.has(post.id) ? 'text-wine' : 'hover:text-wine'
                ]"
              >
                <span>{{ likedPosts.has(post.id) ? '❤️' : '🤍' }}</span>
                <span>{{ post.likesCount }}</span>
              </button>
              <button class="flex items-center gap-2 hover:text-wine transition">
                <span>💬</span>
                <span>{{ post.commentsCount }}</span>
              </button>
              <button
                @click="unsavePost(post.id)"
                class="flex items-center gap-2 hover:text-wine transition"
              >
                <span>🔖</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const savedPosts = ref([])
const loading = ref(true)
const likedPosts = ref(new Set())

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function formatDate(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Agora'
  if (diffMins < 60) return `${diffMins}m`
  if (diffHours < 24) return `${diffHours}h`
  if (diffDays < 7) return `${diffDays}d`
  return date.toLocaleDateString('pt-BR')
}

async function fetchSavedPosts() {
  try {
    const response = await fetch(`${API_BASE}/saved-posts`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      savedPosts.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching saved posts:', error)
  } finally {
    loading.value = false
  }
}

async function toggleLike(postId) {
  try {
    if (likedPosts.value.has(postId)) {
      // Unlike
      const response = await fetch(`${API_BASE}/posts/${postId}/like`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      
      if (response.ok) {
        likedPosts.value.delete(postId)
        const post = savedPosts.value.find(p => p.id === postId)
        if (post) post.likesCount--
      }
    } else {
      // Like
      const response = await fetch(`${API_BASE}/posts/${postId}/like`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      
      if (response.ok) {
        likedPosts.value.add(postId)
        const post = savedPosts.value.find(p => p.id === postId)
        if (post) post.likesCount++
      }
    }
  } catch (error) {
    console.error('Error toggling like:', error)
  }
}

async function unsavePost(postId) {
  try {
    const response = await fetch(`${API_BASE}/posts/${postId}/save`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      savedPosts.value = savedPosts.value.filter(p => p.id !== postId)
    }
  } catch (error) {
    console.error('Error unsaving post:', error)
  }
}

onMounted(async () => {
  await fetchSavedPosts()
})
</script>
