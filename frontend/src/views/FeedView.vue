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
                <input
                  ref="imageInput"
                  type="file"
                  multiple
                  accept="image/*"
                  @change="handleImageUpload"
                  class="hidden"
                />
                <button
                  @click="$refs.imageInput.click()"
                  class="p-2 rounded-full hover:bg-slate-100 transition text-slate-500"
                  title="Adicionar imagens (máx. 4)"
                >
                  📷
                </button>
                <button class="p-2 rounded-full hover:bg-slate-100 transition text-slate-500">🔗</button>
              </div>
              <div class="flex gap-2 items-center">
                <div v-if="selectedImages.length > 0" class="flex gap-2">
                  <div
                    v-for="(img, idx) in selectedImages"
                    :key="idx"
                    class="relative w-12 h-12 rounded-lg overflow-hidden"
                  >
                    <img :src="img.preview" class="w-full h-full object-cover" />
                    <button
                      @click="removeImage(idx)"
                      class="absolute top-0 right-0 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full"
                    >
                      ×
                    </button>
                  </div>
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
                <button
                  @click="toggleComments(post.id)"
                  class="flex items-center gap-2 hover:text-wine transition"
                >
                  <span>💬</span>
                  <span>{{ post.commentsCount }}</span>
                </button>
                <button
                  @click="toggleSave(post.id)"
                  :class="[
                    'flex items-center gap-2 transition',
                    savedPosts.has(post.id) ? 'text-wine' : 'hover:text-wine'
                  ]"
                >
                  <span>{{ savedPosts.has(post.id) ? '🔖' : '🔗' }}</span>
                </button>
              </div>

              <!-- Comments Section -->
              <div v-if="expandedComments.has(post.id)" class="mt-4 pt-4 border-t border-slate-100">
                <div class="space-y-3 mb-4">
                  <div
                    v-for="comment in postComments[post.id] || []"
                    :key="comment.id"
                    class="flex gap-3"
                  >
                    <div class="w-8 h-8 rounded-full bg-malva flex items-center justify-center text-white text-sm flex-shrink-0">
                      {{ comment.authorName?.charAt(0).toUpperCase() || 'U' }}
                    </div>
                    <div class="flex-1">
                      <div class="bg-slate-100 rounded-lg p-3">
                        <p class="font-medium text-sm text-slate-900">{{ comment.authorName }}</p>
                        <p class="text-sm text-slate-700 mt-1">{{ comment.content }}</p>
                      </div>
                      <p class="text-xs text-slate-400 mt-1">{{ formatDate(comment.createdAt) }}</p>
                    </div>
                  </div>
                </div>

                <!-- Add Comment -->
                <div class="flex gap-3">
                  <input
                    v-model="newComments[post.id]"
                    @keyup.enter="submitComment(post.id)"
                    type="text"
                    placeholder="Adicione um comentário..."
                    class="flex-1 px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine text-sm"
                  />
                  <button
                    @click="submitComment(post.id)"
                    :disabled="!newComments[post.id]?.trim()"
                    class="px-4 py-2 rounded-lg bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50 text-sm"
                  >
                    Enviar
                  </button>
                </div>
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
              <router-link
                :to="`/profile/${user.id}`"
                class="font-medium text-sm text-slate-700 truncate hover:text-wine"
              >
                {{ user.name }}
              </router-link>
              <p class="text-xs text-slate-400 truncate">{{ user.institution }}</p>
            </div>
            <button 
              @click="followUser(user.id)"
              class="px-3 py-1 rounded-full border border-wine text-wine text-sm hover:bg-wine hover:text-white transition"
            >
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
const likedPosts = ref(new Set())
const savedPosts = ref(new Set())
const expandedComments = ref(new Set())
const postComments = ref({})
const newComments = ref({})
const selectedImages = ref([])
const imageInput = ref(null)

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function handleImageUpload(event) {
  const files = Array.from(event.target.files)
  
  // Limita a 4 imagens
  const remainingSlots = 4 - selectedImages.value.length
  const filesToAdd = files.slice(0, remainingSlots)
  
  filesToAdd.forEach(file => {
    // Valida tipo
    if (!file.type.startsWith('image/')) {
      alert('Por favor, selecione apenas imagens')
      return
    }
    
    // Valida tamanho (máximo 2MB por imagem)
    if (file.size > 2 * 1024 * 1024) {
      alert('Cada imagem deve ter no máximo 2MB')
      return
    }
    
    // Lê arquivo e cria preview
    const reader = new FileReader()
    reader.onload = (e) => {
      selectedImages.value.push({
        file,
        preview: e.target.result
      })
    }
    reader.readAsDataURL(file)
  })
  
  // Limpa input
  event.target.value = ''
}

function removeImage(index) {
  selectedImages.value.splice(index, 1)
}

async function submitPost() {
  if (!newPostContent.value.trim() && selectedImages.value.length === 0) return
  
  // Converte imagens para base64
  const images = []
  for (const img of selectedImages.value) {
    images.push(img.preview)
  }
  
  const result = await postsStore.createPost(newPostContent.value, images, auth.token)
  if (result) {
    newPostContent.value = ''
    selectedImages.value = []
  }
}

async function fetchSuggestedUsers() {
  try {
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

async function followUser(userId) {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}/follow`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    if (response.ok) {
      // Remove user from suggestions
      suggestedUsers.value = suggestedUsers.value.filter(u => u.id !== userId)
    }
  } catch (error) {
    console.error('Error following user:', error)
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
        const post = postsStore.posts.find(p => p.id === postId)
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
        const post = postsStore.posts.find(p => p.id === postId)
        if (post) post.likesCount++
      }
    }
  } catch (error) {
    console.error('Error toggling like:', error)
  }
}

async function toggleSave(postId) {
  try {
    if (savedPosts.value.has(postId)) {
      // Unsave
      const response = await fetch(`${API_BASE}/posts/${postId}/save`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      
      if (response.ok) {
        savedPosts.value.delete(postId)
      }
    } else {
      // Save
      const response = await fetch(`${API_BASE}/posts/${postId}/save`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      
      if (response.ok) {
        savedPosts.value.add(postId)
      }
    }
  } catch (error) {
    console.error('Error toggling save:', error)
  }
}

async function toggleComments(postId) {
  if (expandedComments.value.has(postId)) {
    expandedComments.value.delete(postId)
  } else {
    expandedComments.value.add(postId)
    await fetchComments(postId)
  }
}

async function fetchComments(postId) {
  try {
    const response = await fetch(`${API_BASE}/posts/${postId}/comments`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      postComments.value[postId] = await response.json()
    }
  } catch (error) {
    console.error('Error fetching comments:', error)
  }
}

async function submitComment(postId) {
  const content = newComments.value[postId]?.trim()
  if (!content) return
  
  try {
    const response = await fetch(`${API_BASE}/posts/${postId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.token}`,
      },
      body: JSON.stringify({ content }),
    })
    
    if (response.ok) {
      const newComment = await response.json()
      if (!postComments.value[postId]) {
        postComments.value[postId] = []
      }
      postComments.value[postId].unshift(newComment)
      newComments.value[postId] = ''
      
      // Incrementa contador
      const post = postsStore.posts.find(p => p.id === postId)
      if (post) post.commentsCount++
    }
  } catch (error) {
    console.error('Error submitting comment:', error)
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
