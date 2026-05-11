const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class ApiError extends Error {
  constructor(message, status, data) {
    super(message)
    this.status = status
    this.data = data
  }
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

  const res = await fetch(`${API_BASE}${endpoint}`, config)

  if (res.status === 401) {
    // token expired or invalid
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    throw new ApiError('Session expired', 401)
  }

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new ApiError(data.detail || 'Something went wrong', res.status, data)
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

// specific API calls
export const auth = {
  googleLogin: (idToken) => api.post('/auth/google', { id_token: idToken }),
  me: () => api.get('/auth/me'),
}

export const chat = {
  send: (message, category = null) =>
    api.post('/chat/', { message, category, stream: false }),
  search: (query, category = null, n_results = 10) =>
    api.post('/chat/search', { query, category, n_results }),
  health: () => api.get('/chat/health'),
}

export const tasks = {
  list: () => api.get('/tasks/me'),
  update: (taskId, data) => api.patch(`/tasks/me/${taskId}`, data),
  progress: () => api.get('/tasks/me/progress'),
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
  me: () => api.get('/users/me'),
  update: (data) => api.patch('/users/me', data),
}
