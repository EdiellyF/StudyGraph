<template>
  <div class="min-h-screen flex">
    <!-- Left Column - Wine/Dark Purple -->
    <div class="w-1/3 bg-wine text-white flex flex-col justify-between p-8">
      <div>
        <h1 class="text-3xl font-bold mb-4">Conecte-se ao conhecimento</h1>
        <p class="text-rose opacity-90">Junte-se à rede social acadêmica e compartilhe ideias com estudantes de todo o Brasil.</p>
      </div>
      <div class="space-y-2 text-sm text-rose opacity-80">
        <p>📚 10k+ estudantes ativos</p>
        <p>🎓 50+ instituições</p>
        <p>💡 5k+ posts compartilhados</p>
      </div>
    </div>

    <!-- Right Column - Cream/Beige -->
    <div class="w-2/3 bg-cream flex items-center justify-center p-8">
      <form @submit.prevent="submitForm" class="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-2xl font-semibold mb-6 text-wine">Criar conta</h2>
        
        <div class="space-y-4">
          <label class="block">
            <span class="text-sm text-slate-700">Nome completo</span>
            <input v-model="form.name" type="text" required class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" placeholder="Seu nome" />
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">Semestre</span>
            <select v-model="form.semester" required class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva bg-white">
              <option value="">Selecione o semestre</option>
              <option v-for="i in 12" :key="i" :value="i">{{ i }}º semestre</option>
            </select>
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">E-mail institucional</span>
            <input v-model="form.email" type="email" required class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" placeholder="seu.email@instituicao.br" />
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">Instituição</span>
            <input v-model="form.institution" type="text" required class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" placeholder="Nome da sua instituição" />
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">Curso</span>
            <input v-model="form.course" type="text" required class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" placeholder="Seu curso" />
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">Senha</span>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              minlength="6" 
              @input="checkPasswordStrength"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" 
              placeholder="Mínimo 6 caracteres"
            />
            <div v-if="form.password" class="mt-2 flex gap-1">
              <div class="h-1 flex-1 rounded" :class="passwordStrength >= 1 ? 'bg-red-400' : 'bg-slate-200'"></div>
              <div class="h-1 flex-1 rounded" :class="passwordStrength >= 2 ? 'bg-yellow-400' : 'bg-slate-200'"></div>
              <div class="h-1 flex-1 rounded" :class="passwordStrength >= 3 ? 'bg-green-400' : 'bg-slate-200'"></div>
            </div>
            <p v-if="form.password" class="mt-1 text-xs" :class="passwordStrengthClass">{{ passwordStrengthText }}</p>
          </label>
        </div>

        <p v-if="auth.error" class="mt-4 text-sm text-red-600">{{ auth.error }}</p>

        <button 
          type="submit" 
          :disabled="auth.loading"
          class="mt-6 w-full rounded-2xl bg-wine px-4 py-3 text-white hover:bg-opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ auth.loading ? 'Cadastrando...' : 'Cadastrar' }}
        </button>

        <p class="mt-4 text-center text-sm text-slate-600">
          Já tem conta? 
          <router-link to="/login" class="text-wine hover:underline">Faça login</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({ 
  name: '', 
  email: '', 
  password: '',
  semester: '',
  institution: '',
  course: ''
})

const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return 0
  
  let strength = 0
  if (password.length >= 6) strength++
  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password) && /[0-9]/.test(password)) strength++
  
  return strength
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength === 0) return ''
  if (strength === 1) return 'Senha fraca'
  if (strength === 2) return 'Senha média'
  return 'Senha forte'
})

const passwordStrengthClass = computed(() => {
  const strength = passwordStrength.value
  if (strength === 1) return 'text-red-500'
  if (strength === 2) return 'text-yellow-500'
  return 'text-green-500'
})

function checkPasswordStrength() {
  // Computed handles this
}

async function submitForm() {
  const success = await auth.register({
    name: form.name,
    email: form.email,
    password: form.password,
    semester: form.semester,
    institution: form.institution,
    course: form.course
  })
  if (success) {
    router.push('/feed')
  }
}
</script>
