<template>
  <section class="space-y-6 text-center">
    <div class="rounded-3xl bg-white p-10 shadow-sm">
      <h1 class="text-4xl font-bold text-wine">StudyGraph</h1>
      <p class="mt-4 text-slate-700">Rede social acadêmica leve, com login seguro e perfil pessoal.</p>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
        <router-link to="/login" class="rounded-2xl bg-wine px-6 py-3 text-white hover:bg-opacity-90">Entrar</router-link>
        <router-link to="/register" class="rounded-2xl border border-wine px-6 py-3 text-wine hover:bg-wine hover:text-white transition">Criar conta</router-link>
      </div>
    </div>
  </section>
</template>
