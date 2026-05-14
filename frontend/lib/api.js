export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class ApiError extends Error {
  constructor(message, status, data) {
    super(message)
    this.status = status
    this.data = data
  }
}

let isRefreshing = false
let refreshPromise = null

async function refreshTokens() {
  const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null
  if (!refreshToken) throw new Error('No refresh token')

  const res = await fetch(`${API_BASE}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })

  if (!res.ok) {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    throw new Error('Refresh failed')
  }

  const data = await res.json()
  localStorage.setItem('token', data.access_token)
  localStorage.setItem('refresh_token', data.refresh_token)
  return data.access_token
}

async function request(endpoint, options = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  }

  let res = await fetch(`${API_BASE}${endpoint}`, config)

  // On 401, try refresh once
  if (res.status === 401 && typeof window !== 'undefined') {
    if (!isRefreshing) {
      isRefreshing = true
      refreshPromise = refreshTokens().catch(() => {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
        throw new ApiError('Session expired', 401)
      }).finally(() => {
        isRefreshing = false
        refreshPromise = null
      })
    }

    if (refreshPromise) {
      const newToken = await refreshPromise
      config.headers['Authorization'] = `Bearer ${newToken}`
      res = await fetch(`${API_BASE}${endpoint}`, config)
    }
  }

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const detail = data.detail
    const message =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
          : 'Something went wrong'
    throw new ApiError(message, res.status, data)
  }

  if (res.status === 204) return null
  return res.json()
}

export const api = {
  get: (endpoint) => request(endpoint),
  post: (endpoint, body) => request(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  patch: (endpoint, body) => request(endpoint, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
}

export const auth = {
  googleLogin: (idToken) => api.post('/auth/google', { token: idToken }),
  emailRegister: (email, password, name, role = 'student') => api.post('/auth/register', { email, password, name, role }),
  emailLogin: (email, password) => api.post('/auth/login', { email, password }),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => api.post('/auth/reset-password', { token, password }),
  me: () => api.get('/auth/me'),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
}

export const chat = {
  send: (message, category = null, conversationId = null) =>
    api.post('/chat/', { message, category, stream: false, conversation_id: conversationId }),
  search: (query, category = null, n_results = 10) =>
    api.post('/chat/search', { query, category, n_results }),
  health: () => api.get('/chat/health'),
}

export const tasks = {
  list: () => api.get('/tasks/my-tasks'),
  update: (taskId, data) => api.patch(`/tasks/my-tasks/${taskId}`, data),
  progress: () => api.get('/tasks/my-progress'),
}

/** Multipart upload (do not set Content-Type — browser sets boundary). */
export async function uploadMultipart(endpoint, formData) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  let headers = {}
  if (token) headers['Authorization'] = `Bearer ${token}`

  let res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers,
    body: formData,
  })

  if (res.status === 401 && typeof window !== 'undefined') {
    if (!isRefreshing) {
      isRefreshing = true
      refreshPromise = refreshTokens().catch(() => {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }).finally(() => {
        isRefreshing = false
        refreshPromise = null
      })
    }
    if (refreshPromise) {
      const newToken = await refreshPromise
      headers['Authorization'] = `Bearer ${newToken}`
      res = await fetch(`${API_BASE}${endpoint}`, { method: 'POST', headers, body: formData })
    }
  }

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const detail = data.detail
    const message =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
          : 'Upload failed'
    throw new ApiError(message, res.status, data)
  }
  return res.json()
}

export const documents = {
  listMine: () => api.get('/documents/my-documents'),
  upload: (formData) => uploadMultipart('/documents/upload', formData),
}

export const admission = {
  getApplication: () => api.get('/admission/application'),
  patchApplication: (body) => api.patch('/admission/application', body),
  assistantChat: (message) => api.post('/admission/assistant/chat', { message }),
}

export const knowledge = {
  list: (category = null) => {
    const params = category ? `?category=${category}` : ''
    return api.get(`/knowledge/entries${params}`)
  },
  ingestDefaults: () => api.post('/knowledge/ingest-defaults'),
  stats: () => api.get('/knowledge/stats'),
}

export const users = {
  me: () => api.get('/auth/me'),
  update: (data) => api.patch('/users/me', data),
}
