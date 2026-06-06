<template>
  <div class="flex gap-6 max-w-6xl mx-auto">
    <!-- Main Feed Column -->
    <div class="flex-1">
      <!-- Create Post -->
      <div class="bg-white rounded-2xl shadow-sm p-6 mb-6">
        <div class="flex gap-4">
          <div class="w-12 h-12 rounded-full bg-wine flex items-center justify-center text-white flex-shrink-0">
            {{ auth.user?.name?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div class="flex-1">
            <textarea
              v-model="newPostContent"
              placeholder="Compartilhe seu conhecimento..."
              class="w-full resize-none border-0 focus:outline-none text-slate-700 placeholder-slate-400 min-h-[100px]"
              rows="3"
            />
            <div class="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
              <div class="flex gap-2">
                <button class="p-2 rounded-full hover:bg-slate-100 transition text-slate-500">📷</button>
                <button class="p-2 rounded-full hover:bg-slate-100 transition text-slate-500">🔗</button>
              </div>
              <button
                @click="submitPost"
                :disabled="!newPostContent.trim() || postsStore.loading"
                class="px-6 py-2 rounded-full bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ postsStore.loading ? 'Publicando...' : 'Publicar' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Posts List -->
      <div v-if="postsStore.loading && postsStore.posts.length === 0" class="text-center py-12 text-slate-500">
        <p>Carregando posts...</p>
      </div>

      <div v-else-if="postsStore.posts.length === 0" class="bg-white rounded-2xl shadow-sm p-12 text-center">
        <p class="text-slate-500 mb-4">Nenhum post ainda.</p>
        <p class="text-slate-400 text-sm">Seja o primeiro a compartilhar algo!</p>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="post in postsStore.posts"
          :key="post.id"
          class="bg-white rounded-2xl shadow-sm p-6"
        >
          <div class="flex gap-4">
            <div class="w-12 h-12 rounded-full bg-wine flex items-center justify-center text-white flex-shrink-0">
              {{ post.authorName?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h3 class="font-semibold text-wine">{{ post.authorName }}</h3>
                <span class="text-slate-400 text-sm">·</span>
                <span class="text-slate-400 text-sm">{{ formatDate(post.createdAt) }}</span>
              </div>
              <p class="text-slate-700 whitespace-pre-wrap mb-4">{{ post.content }}</p>
              <div class="flex items-center gap-6 text-slate-500">
                <button class="flex items-center gap-2 hover:text-wine transition">
                  <span>❤️</span>
                  <span>{{ post.likesCount }}</span>
                </button>
                <button class="flex items-center gap-2 hover:text-wine transition">
                  <span>💬</span>
                  <span>{{ post.commentsCount }}</span>
                </button>
                <button class="flex items-center gap-2 hover:text-wine transition">
                  <span>🔖</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Sidebar - Suggested Users -->
    <div class="w-80 flex-shrink-0">
      <div class="bg-white rounded-2xl shadow-sm p-6 sticky top-24">
        <h3 class="font-semibold text-wine mb-4">Sugeridos para você</h3>
        
        <div v-if="suggestedUsers.length === 0" class="text-center py-8 text-slate-500 text-sm">
          <p>Carregando sugestões...</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="user in suggestedUsers"
            :key="user.id"
            class="flex items-center gap-3"
          >
            <div class="w-10 h-10 rounded-full bg-malva flex items-center justify-center text-white flex-shrink-0">
              {{ user.name?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-sm text-slate-700 truncate">{{ user.name }}</p>
              <p class="text-xs text-slate-400 truncate">{{ user.institution }}</p>
            </div>
            <button class="px-3 py-1 rounded-full border border-wine text-wine text-sm hover:bg-wine hover:text-white transition">
              Seguir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { usePostsStore } from '../stores/posts'

const auth = useAuthStore()
const postsStore = usePostsStore()
const newPostContent = ref('')
const suggestedUsers = ref([])

async function submitPost() {
  if (!newPostContent.value.trim()) return
  
  const result = await postsStore.createPost(newPostContent.value, auth.token)
  if (result) {
    newPostContent.value = ''
  }
}

async function fetchSuggestedUsers() {
  try {
    const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    const response = await fetch(`${API_BASE}/users/suggested`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      suggestedUsers.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching suggested users:', error)
  }
}

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

onMounted(async () => {
  await postsStore.fetchPosts(auth.token)
  await fetchSuggestedUsers()
})
</script>
