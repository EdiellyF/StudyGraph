<template>
  <section class="max-w-4xl mx-auto space-y-6">
    <!-- Profile Header -->
    <div class="rounded-3xl bg-white p-8 shadow-sm">
      <div v-if="!auth.isAuthenticated" class="text-slate-600">
        <p>Você precisa estar logado para ver seu perfil.</p>
        <router-link to="/login" class="mt-4 inline-block rounded-2xl bg-wine px-5 py-3 text-white">
          Ir para login
        </router-link>
      </div>

      <div v-else-if="loadingProfile" class="text-slate-600 py-12 text-center">
        <p>Carregando perfil...</p>
      </div>

      <div v-else-if="profileUser">
        <!-- Profile Info -->
        <div class="flex items-start justify-between mb-8">
          <div class="flex items-start gap-4">
            <div class="w-24 h-24 rounded-full bg-wine flex items-center justify-center text-white text-4xl flex-shrink-0">
              {{ profileUser.name?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div>
              <h1 class="text-3xl font-bold text-wine">{{ profileUser.name }}</h1>
              <p class="text-slate-600 mt-1">@{{ profileUser.name?.toLowerCase().replace(/\s/g, '') || 'user' }}</p>
              <p class="text-slate-700 mt-3 max-w-2xl">{{ profileUser.bio || 'Sem descrição adicionada.' }}</p>
              <p class="text-slate-500 text-sm mt-2">{{ profileUser.institution }} • {{ profileUser.course }}</p>
            </div>
          </div>

          <!-- Action Button -->
          <button
            v-if="isOwnProfile"
            @click="isEditingBio = !isEditingBio"
            class="px-6 py-2 rounded-full border border-wine text-wine hover:bg-wine hover:text-white transition"
          >
            {{ isEditingBio ? 'Cancelar' : 'Editar Perfil' }}
          </button>
          <button
            v-else
            @click="toggleFollow"
            :disabled="followLoading"
            class="px-6 py-2 rounded-full transition disabled:opacity-50"
            :class="isFollowing ? 'border border-wine text-wine hover:bg-wine hover:text-white' : 'bg-wine text-white hover:bg-opacity-90'"
          >
            {{ followLoading ? 'Carregando...' : isFollowing ? 'Deixar de Seguir' : 'Seguir' }}
          </button>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-4 mb-8 pt-8 border-t border-slate-100">
          <div class="text-center">
            <p class="text-2xl font-bold text-wine">{{ postsCount }}</p>
            <p class="text-slate-600 text-sm">Posts</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-wine">{{ profileUser.followersCount || 0 }}</p>
            <p class="text-slate-600 text-sm">Seguidores</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-wine">{{ profileUser.followingCount || 0 }}</p>
            <p class="text-slate-600 text-sm">Seguindo</p>
          </div>
        </div>

        <!-- Bio Edit Section (só se for próprio perfil) -->
        <div v-if="isOwnProfile && isEditingBio" class="bg-cream rounded-2xl p-6 mb-8">
          <textarea
            v-model="editingBio"
            placeholder="Adicione uma bio..."
            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-malva resize-none"
            rows="3"
          />
          <div class="flex gap-2 mt-4 justify-end">
            <button
              @click="isEditingBio = false"
              class="px-4 py-2 rounded-full border border-slate-300 hover:bg-slate-100 transition"
            >
              Cancelar
            </button>
            <button
              @click="saveBio"
              :disabled="savingBio"
              class="px-4 py-2 rounded-full bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50"
            >
              {{ savingBio ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-slate-600 py-12 text-center">
        <p>Perfil não encontrado.</p>
      </div>
    </div>

    <!-- Posts Section -->
    <div v-if="profileUser && postsCount > 0">
      <h2 class="text-2xl font-bold text-wine mb-4">Posts</h2>
      
      <div v-if="loadingPosts" class="text-center py-12 text-slate-500">
        <p>Carregando posts...</p>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="post in userPosts"
          :key="post.id"
          class="bg-white rounded-2xl shadow-sm p-6"
        >
          <div class="flex gap-4">
            <div class="w-12 h-12 rounded-full bg-wine flex items-center justify-center text-white flex-shrink-0">
              {{ profileUser.name?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h3 class="font-semibold text-wine">{{ profileUser.name }}</h3>
                <span class="text-slate-400 text-sm">·</span>
                <span class="text-slate-400 text-sm">{{ formatDate(post.createdAt) }}</span>
              </div>
              <p class="text-slate-700 whitespace-pre-wrap mb-4">{{ post.content }}</p>
              <div class="flex items-center gap-6 text-slate-500">
                <button class="flex items-center gap-2 hover:text-wine transition">
                  <span>❤️</span>
                  <span>{{ post.likesCount || 0 }}</span>
                </button>
                <button class="flex items-center gap-2 hover:text-wine transition">
                  <span>💬</span>
                  <span>{{ post.commentsCount || 0 }}</span>
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

    <div v-else-if="profileUser" class="bg-white rounded-2xl shadow-sm p-12 text-center">
      <p class="text-slate-500 mb-4">Nenhum post ainda.</p>
      <p class="text-slate-400 text-sm">{{ isOwnProfile ? 'Seja o primeiro a compartilhar algo!' : 'Este usuário ainda não compartilhou nada.' }}</p>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRoute } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()

const profileUser = ref(null)
const userPosts = ref([])
const loadingProfile = ref(true)
const loadingPosts = ref(false)
const isEditingBio = ref(false)
const editingBio = ref('')
const savingBio = ref(false)
const followLoading = ref(false)
const isFollowing = ref(false)

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const isOwnProfile = computed(() => {
  if (!auth.user || !profileUser.value) return false
  return auth.user.id === profileUser.value.id
})

const postsCount = computed(() => userPosts.value.length)

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

async function fetchProfileData() {
  try {
    loadingProfile.value = true
    
    // Get profile data
    const profileResponse = await fetch(`${API_BASE}/profile/me`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (profileResponse.ok) {
      profileUser.value = await profileResponse.json()
      editingBio.value = profileUser.value.bio || ''
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  } finally {
    loadingProfile.value = false
  }
}

async function fetchUserPosts() {
  try {
    loadingPosts.value = true
    
    // Get user's posts
    const postsResponse = await fetch(`${API_BASE}/posts?user_id=${profileUser.value.id}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (postsResponse.ok) {
      userPosts.value = await postsResponse.json()
    }
  } catch (error) {
    console.error('Error fetching user posts:', error)
  } finally {
    loadingPosts.value = false
  }
}

async function saveBio() {
  try {
    savingBio.value = true
    
    const response = await fetch(`${API_BASE}/profile/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.token}`,
      },
      body: JSON.stringify({ bio: editingBio.value }),
    })

    if (response.ok) {
      profileUser.value = await response.json()
      isEditingBio.value = false
    }
  } catch (error) {
    console.error('Error saving bio:', error)
  } finally {
    savingBio.value = false
  }
}

async function toggleFollow() {
  try {
    followLoading.value = true
    
    if (isFollowing.value) {
      // Unfollow
      await fetch(`${API_BASE}/users/${profileUser.value.id}/follow`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
    } else {
      // Follow
      await fetch(`${API_BASE}/users/${profileUser.value.id}/follow`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${auth.token}` },
      })
    }
    
    isFollowing.value = !isFollowing.value
  } catch (error) {
    console.error('Error toggling follow:', error)
  } finally {
    followLoading.value = false
  }
}

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) {
    await auth.fetchProfile()
  }
  
  await fetchProfileData()
  await fetchUserPosts()
})
</script>
