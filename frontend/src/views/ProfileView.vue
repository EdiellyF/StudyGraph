<template>
  <section class="space-y-6">
    <div class="rounded-3xl bg-white p-8 shadow-sm">
      <h2 class="text-3xl font-semibold mb-4">Meu Perfil</h2>

      <div v-if="!auth.isAuthenticated" class="text-slate-600">
        <p>Você precisa estar logado para ver seu perfil.</p>
        <router-link to="/login" class="mt-4 inline-block rounded-2xl bg-slate-900 px-5 py-3 text-white">Ir para login</router-link>
      </div>

      <div v-else-if="!profileLoaded" class="text-slate-600">Carregando...</div>

      <div v-else class="space-y-4">
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="rounded-2xl border p-5 bg-slate-50">
            <p class="text-sm uppercase tracking-[0.2em] text-slate-500">Nome</p>
            <p class="mt-2 text-lg font-medium">{{ auth.user.name }}</p>
          </div>
          <div class="rounded-2xl border p-5 bg-slate-50">
            <p class="text-sm uppercase tracking-[0.2em] text-slate-500">Email</p>
            <p class="mt-2 text-lg font-medium">{{ auth.user.email }}</p>
          </div>
          <div class="rounded-2xl border p-5 bg-slate-50">
            <p class="text-sm uppercase tracking-[0.2em] text-slate-500">Curso</p>
            <p class="mt-2 text-lg font-medium">{{ auth.user.course || 'Não informado' }}</p>
          </div>
          <div class="rounded-2xl border p-5 bg-slate-50">
            <p class="text-sm uppercase tracking-[0.2em] text-slate-500">Instituição</p>
            <p class="mt-2 text-lg font-medium">{{ auth.user.institution || 'Não informada' }}</p>
          </div>
        </div>

        <div class="rounded-2xl border p-5 bg-slate-50">
          <p class="text-sm uppercase tracking-[0.2em] text-slate-500">Bio</p>
          <p class="mt-2 text-slate-700">{{ auth.user.bio || 'Sem descrição adicionada.' }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const profileLoaded = ref(false)

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) {
    await auth.fetchProfile()
  }
  profileLoaded.value = true
})
</script>
