<template>
  <form @submit.prevent="submitForm" class="max-w-md mx-auto bg-white rounded-2xl border p-6 shadow-sm">
    <h2 class="text-2xl font-semibold mb-4">Entrar</h2>
    <div class="space-y-4">
      <label class="block">
        <span class="text-sm text-slate-700">Email</span>
        <input v-model="form.email" type="email" required class="mt-1 w-full rounded-xl border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400" />
      </label>
      <label class="block">
        <span class="text-sm text-slate-700">Senha</span>
        <input v-model="form.password" type="password" required class="mt-1 w-full rounded-xl border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400" />
      </label>
    </div>

    <p v-if="auth.error" class="mt-4 text-sm text-red-600">{{ auth.error }}</p>

    <button type="submit" class="mt-6 w-full rounded-2xl bg-slate-900 px-4 py-3 text-white hover:bg-slate-700">Entrar</button>
  </form>
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
  if (success) {
    router.push('/feed')
  }
}
</script>
