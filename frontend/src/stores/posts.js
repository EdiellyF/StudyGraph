import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchPosts(token) {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/posts`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (!response.ok) {
        throw new Error('Falha ao carregar posts')
      }

      const data = await response.json()
      posts.value = data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createPost(content, token) {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content }),
      })

      if (!response.ok) {
        throw new Error('Falha ao criar post')
      }

      const newPost = await response.json()
      posts.value.unshift(newPost)
      return newPost
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    posts,
    loading,
    error,
    fetchPosts,
    createPost,
  }
})
