const API_URL = import.meta.env.VITE_API_URL ?? 'https://studybot-55s2.vercel.app/api/v1'

export async function api(path, options = {}) {
  const token = localStorage.getItem('studybot_token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  }

  const response = await fetch(`${API_URL}${path}`, {
    credentials: 'include',
    ...options,
    headers,
  })
  let body
  try {
    body = await response.json()
  } catch {
    body = { message: response.statusText || 'Request failed' }
  }
  if (!response.ok) {
    throw new Error(body?.detail || body?.message || 'Request failed')
  }
  return body.data
}

export const studybotApi = {
  login: async (email, password) => {
    const data = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
    if (data?.token) {
      localStorage.setItem('studybot_token', data.token)
    }
    return data
  },
  currentUser: () => api('/auth/me'),
  logout: async () => {
    try {
      await api('/auth/logout', { method: 'POST' })
    } finally {
      localStorage.removeItem('studybot_token')
    }
  },
  topics: () => api('/topics'),
  progress: () => api('/progress/overview'),
  startPractice: (payload) => api('/practice/start', { method: 'POST', body: JSON.stringify(payload) }),
  startMockTest: (payload) => api('/mock-tests/start', { method: 'POST', body: JSON.stringify(payload) }),
  getTest: (testId) => api(`/tests/${testId}`),
  submitTest: (testId, answers) => api(`/tests/${testId}/submit`, { method: 'POST', body: JSON.stringify({ answers }) }),
  result: (testId) => api(`/tests/${testId}/result`),
  review: (testId) => api(`/tests/${testId}/review`),
  wrongAnswers: (topicId) => api(`/revision/wrong-answers${topicId ? `?topic_id=${topicId}` : ''}`),
  startRevision: (payload) => api('/revision/start', { method: 'POST', body: JSON.stringify(payload) }),
  topicProgress: () => api('/progress/topics'),
  weakTopics: () => api('/progress/weak-topics'),
}
