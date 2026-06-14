<template>
  <section class="max-w-2xl mx-auto">
    <div class="bg-white rounded-2xl shadow-sm">
      <div class="p-6 border-b border-slate-100">
        <h1 class="text-2xl font-bold text-wine">Configurações</h1>
      </div>

      <div class="p-6 space-y-6">
        <!-- Avatar Upload -->
        <div>
          <h2 class="text-lg font-semibold text-slate-900 mb-4">Avatar</h2>
          <div class="space-y-4">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-full bg-wine flex items-center justify-center text-white text-2xl flex-shrink-0">
                {{ auth.user?.name?.charAt(0).toUpperCase() || 'U' }}
              </div>
              <div>
                <input
                  ref="avatarInput"
                  type="file"
                  accept="image/png,image/jpeg,image/jpg"
                  @change="handleAvatarUpload"
                  class="hidden"
                />
                <button
                  @click="$refs.avatarInput.click()"
                  :disabled="uploadingAvatar"
                  class="px-6 py-2 rounded-full bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50"
                >
                  {{ uploadingAvatar ? 'Enviando...' : 'Alterar Avatar' }}
                </button>
                <p class="text-xs text-slate-500 mt-2">PNG ou JPEG, máximo 2MB</p>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-slate-100"></div>

        <!-- Profile Settings -->
        <div>
          <h2 class="text-lg font-semibold text-slate-900 mb-4">Perfil</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Nome</label>
              <input
                v-model="profileForm.name"
                type="text"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Email</label>
              <input
                v-model="profileForm.email"
                type="email"
                disabled
                class="w-full px-4 py-2 rounded-lg border border-slate-200 bg-slate-50 text-slate-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Instituição</label>
              <input
                v-model="profileForm.institution"
                type="text"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Curso</label>
              <input
                v-model="profileForm.course"
                type="text"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Semestre</label>
              <input
                v-model="profileForm.semester"
                type="text"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Bio</label>
              <textarea
                v-model="profileForm.bio"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-wine resize-none"
                rows="3"
              />
            </div>
            <button
              @click="saveProfile"
              :disabled="savingProfile"
              class="w-full px-6 py-2 rounded-full bg-wine text-white hover:bg-opacity-90 transition disabled:opacity-50"
            >
              {{ savingProfile ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </div>

        <div class="border-t border-slate-100"></div>

        <!-- Preferences -->
        <div>
          <h2 class="text-lg font-semibold text-slate-900 mb-4">Preferências</h2>
          <div class="space-y-4">
            <label class="flex items-center gap-3 cursor-pointer">
              <input
                v-model="preferences.emailNotifications"
                type="checkbox"
                class="w-4 h-4 rounded border-slate-300 text-wine focus:ring-wine"
              />
              <span class="text-slate-700">Receber notificações por email</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer">
              <input
                v-model="preferences.privateProfile"
                type="checkbox"
                class="w-4 h-4 rounded border-slate-300 text-wine focus:ring-wine"
              />
              <span class="text-slate-700">Perfil privado</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer">
              <input
                v-model="preferences.allowMessages"
                type="checkbox"
                class="w-4 h-4 rounded border-slate-300 text-wine focus:ring-wine"
              />
              <span class="text-slate-700">Permitir mensagens diretas</span>
            </label>
          </div>
        </div>

        <div class="border-t border-slate-100"></div>

        <!-- Account -->
        <div>
          <h2 class="text-lg font-semibold text-slate-900 mb-4">Conta</h2>
          <div class="space-y-4">
            <button
              @click="logout"
              class="w-full px-6 py-2 rounded-full border border-slate-300 text-slate-700 hover:bg-slate-50 transition"
            >
              Fazer Logout
            </button>
            <button
              @click="deleteAccount"
              :disabled="deletingAccount"
              class="w-full px-6 py-2 rounded-full border border-red-300 text-red-600 hover:bg-red-50 transition disabled:opacity-50"
            >
              {{ deletingAccount ? 'Deletando...' : 'Deletar Conta' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const profileForm = ref({
  name: '',
  email: '',
  institution: '',
  course: '',
  semester: '',
  bio: ''
})

const preferences = ref({
  emailNotifications: true,
  privateProfile: false,
  allowMessages: true
})

const savingProfile = ref(false)
const deletingAccount = ref(false)
const uploadingAvatar = ref(false)
const avatarInput = ref(null)

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function handleAvatarUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  
  // Valida tipo
  if (!['image/png', 'image/jpeg', 'image/jpg'].includes(file.type)) {
    alert('Por favor, selecione um arquivo PNG ou JPEG')
    return
  }
  
  // Valida tamanho (máximo 2MB)
  if (file.size > 2 * 1024 * 1024) {
    alert('O arquivo deve ter no máximo 2MB')
    return
  }
  
  try {
    uploadingAvatar.value = true
    
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${API_BASE}/profile/me/avatar`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.token}` },
      body: formData
    })
    
    if (response.ok) {
      await auth.fetchProfile()
      alert('Avatar atualizado com sucesso!')
    } else {
      const error = await response.json()
      alert(`Erro: ${error.detail || 'Falha ao atualizar avatar'}`)
    }
  } catch (error) {
    console.error('Error uploading avatar:', error)
    alert('Erro ao enviar avatar')
  } finally {
    uploadingAvatar.value = false
    event.target.value = ''
  }
}

async function loadProfile() {
  try {
    const response = await fetch(`${API_BASE}/profile/me`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    
    if (response.ok) {
      const user = await response.json()
      profileForm.value = {
        name: user.name || '',
        email: user.email || '',
        institution: user.institution || '',
        course: user.course || '',
        semester: user.semester || '',
        bio: user.bio || ''
      }
    }
  } catch (error) {
    console.error('Error loading profile:', error)
  }
}

async function saveProfile() {
  try {
    savingProfile.value = true
    
    const response = await fetch(`${API_BASE}/profile/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.token}`,
      },
      body: JSON.stringify({
        name: profileForm.value.name,
        institution: profileForm.value.institution,
        course: profileForm.value.course,
        semester: profileForm.value.semester,
        bio: profileForm.value.bio
      }),
    })

    if (response.ok) {
      await auth.fetchProfile()
      alert('Perfil atualizado com sucesso!')
    } else {
      const error = await response.json()
      alert(`Erro: ${error.detail || 'Falha ao atualizar perfil'}`)
    }
  } catch (error) {
    console.error('Error saving profile:', error)
    alert('Erro ao salvar perfil')
  } finally {
    savingProfile.value = false
  }
}

async function logout() {
  auth.logout()
  router.push('/login')
}

async function deleteAccount() {
  if (!confirm('Tem certeza que deseja deletar sua conta? Esta ação é irreversível.')) {
    return
  }

  try {
    deletingAccount.value = true
    
    const response = await fetch(`${API_BASE}/profile/me`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    if (response.ok) {
      auth.logout()
      router.push('/')
      alert('Conta deletada com sucesso')
    }
  } catch (error) {
    console.error('Error deleting account:', error)
    alert('Erro ao deletar conta')
  } finally {
    deletingAccount.value = false
  }
}

onMounted(async () => {
  await loadProfile()
})
</script>
