import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('studygraph_token') || '')
  const user = ref(null)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function saveToken(newToken) {
    token.value = newToken
    localStorage.setItem('studygraph_token', newToken)
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('studygraph_token')
  }

  async function login(payload) {
    error.value = null
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const data = await response.json()
      error.value = data.detail || 'Falha no login'
      return false
    }

    const data = await response.json()
    saveToken(data.access_token)
    await fetchProfile()
    return true
  }

  async function register(payload) {
    error.value = null
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const data = await response.json()
      error.value = data.detail || 'Falha no cadastro'
      return false
    }

    await login({ email: payload.email, password: payload.password })
    return true
  }

  async function fetchProfile() {
    if (!token.value) {
      return null
    }

    const response = await fetch(`${API_BASE}/profile/me`, {
      headers: { Authorization: `Bearer ${token.value}` },
    })

    if (!response.ok) {
      logout()
      return null
    }

    const data = await response.json()
    user.value = data
    return data
  }

  return {
    token,
    user,
    error,
    isAuthenticated,
    login,
    logout,
    register,
    fetchProfile,
  }
})
