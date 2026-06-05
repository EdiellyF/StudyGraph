<template>
  <section class="space-y-6 text-center">
    <div class="rounded-3xl bg-white p-10 shadow-sm">
      <h1 class="text-4xl font-bold text-slate-900">StudyGraph</h1>
      <p class="mt-4 text-slate-600">Rede social acadêmica leve, com login seguro e perfil pessoal.</p>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
        <router-link to="/login" class="rounded-2xl bg-slate-900 px-6 py-3 text-white hover:bg-slate-700">Entrar</router-link>
        <router-link to="/register" class="rounded-2xl border border-slate-300 px-6 py-3 text-slate-900 hover:bg-slate-50">Criar conta</router-link>
      </div>
    </div>
  </section>
</template>
