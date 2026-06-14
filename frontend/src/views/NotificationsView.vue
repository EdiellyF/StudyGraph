<template>
  <section class="max-w-2xl mx-auto">
    <div class="bg-white rounded-2xl shadow-sm">
      <div class="p-6 border-b border-slate-100">
        <h1 class="text-2xl font-bold text-wine">Notificações</h1>
      </div>

      <div v-if="loading" class="p-12 text-center text-slate-500">
        <p>Carregando notificações...</p>
      </div>

      <div v-else-if="notifications.length === 0" class="p-12 text-center">
        <p class="text-slate-500 mb-4">Nenhuma notificação ainda.</p>
        <p class="text-slate-400 text-sm">Quando alguém curtir ou comentar seus posts, você verá aqui.</p>
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div
          v-for="notif in notifications"
          :key="notif.id"
          @click="markAsRead(notif.id)"
          :class="[
            'p-6 cursor-pointer transition hover:bg-slate-50',
            !notif.read ? 'bg-cream' : ''
          ]"
        >
          <div class="flex gap-4">
            <div class="w-12 h-12 rounded-full bg-wine flex items-center justify-center text-white flex-shrink-0">
              {{ notif.fromUserName?.charAt(0).toUpperCase() || 'U' }}
            </div>
            <div class="flex-1">
              <p class="text-slate-700">
                <span class="font-semibold text-wine">{{ notif.fromUserName }}</span>
                {{ notif.message }}
              </p>
              <p class="text-slate-400 text-sm mt-1">{{ formatDate(notif.createdAt) }}</p>
            </div>
            <div v-if="!notif.read" class="w-3 h-3 rounded-full bg-wine flex-shrink-0 mt-2"></div>
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
const notifications = ref([])
const loading = ref(true)

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

async function fetchNotifications() {
  try {
    const response = await fetch(`${API_BASE}/notifications`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      notifications.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching notifications:', error)
  } finally {
    loading.value = false
  }
}

async function markAsRead(notificationId) {
  try {
    await fetch(`${API_BASE}/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    const notif = notifications.value.find(n => n.id === notificationId)
    if (notif) {
      notif.read = true
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

onMounted(async () => {
  await fetchNotifications()
})
</script>
