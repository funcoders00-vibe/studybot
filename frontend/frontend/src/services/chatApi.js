import { api } from './api'

export const chatApi = {
  createSession: (title) => api('/chat/sessions', { method: 'POST', body: JSON.stringify({ title }) }),
  listSessions: () => api('/chat/sessions'),
  getSession: (sessionId) => api(`/chat/sessions/${sessionId}`),
  deleteSession: (sessionId) => api(`/chat/sessions/${sessionId}`, { method: 'DELETE' }),
  sendMessage: (sessionId, message) => api(`/chat/${sessionId}/message`, { method: 'POST', body: JSON.stringify({ message }) }),
}
