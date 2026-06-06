<template>
  <div class="min-h-screen flex">
    <!-- Left Column - Wine/Dark Purple -->
    <div class="w-1/3 bg-wine text-white flex flex-col justify-between p-8">
      <div>
        <h1 class="text-3xl font-bold mb-4">Bem-vindo de volta</h1>
        <p class="text-rose opacity-90">Acesse a comunidade acadêmica e continue compartilhando conhecimento.</p>
      </div>
      <div class="space-y-2 text-sm text-rose opacity-80">
        <p>📚 10k+ estudantes ativos</p>
        <p>🎓 50+ instituições</p>
        <p>💡 5k+ posts compartilhados</p>
      </div>
    </div>

    <!-- Right Column - Cream/Beige -->
    <div class="w-2/3 bg-cream flex items-center justify-center p-8">
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-2xl font-semibold mb-6 text-wine">Fazer login</h2>
        
        <form @submit.prevent="submitForm" class="space-y-4">
          <label class="block">
            <span class="text-sm text-slate-700">E-mail institucional</span>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" 
              placeholder="seu.email@instituicao.br"
            />
          </label>

          <label class="block">
            <span class="text-sm text-slate-700">Senha</span>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-malva" 
              placeholder="••••••••"
            />
          </label>

          <div v-if="auth.error" class="mt-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-sm">
            {{ auth.error }}
          </div>

          <button 
            type="submit" 
            :disabled="auth.loading"
            class="mt-6 w-full rounded-2xl bg-wine px-4 py-3 text-white hover:bg-opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ auth.loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <p class="mt-4 text-center text-sm text-slate-600">
          Não tem conta? 
          <router-link to="/register" class="text-wine hover:underline">Faça seu cadastro</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({ email: '', password: '' })

async function submitForm() {
  const success = await auth.login({ email: form.email, password: form.password })
  if (success) router.push('/feed')
}
</script>
