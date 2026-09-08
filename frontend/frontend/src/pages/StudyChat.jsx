import { useEffect, useState } from 'react'
import { chatApi } from '../services/chatApi'
import ChatSidebar from '../components/chat/ChatSidebar'
import ChatWindow from '../components/chat/ChatWindow'
import '../styles/chat.css'

export default function StudyChat({ setPage, setPracticePrefill, setMockTestPrefill }) {
  const [sessions, setSessions] = useState([])
  const [activeSessionId, setActiveSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    chatApi.listSessions()
      .then((data) => {
        setSessions(data || [])
        if (data && data.length > 0) {
          loadSession(data[0].id)
        } else {
          // Automatically create initial session
          chatApi.createSession('New Study Session')
            .then((newSession) => {
              setSessions([newSession])
              setActiveSessionId(newSession.id)
              setMessages([])
            })
            .catch((err) => setError(err.message))
        }
      })
      .catch((err) => setError(err.message))
  }, [])

  function loadSession(sessionId) {
    setActiveSessionId(sessionId)
    chatApi.getSession(sessionId)
      .then((data) => {
        setMessages(data.messages || [])
      })
      .catch((err) => setError(err.message))
  }

  async function handleNewChat() {
    try {
      const newSession = await chatApi.createSession('New Study Session')
      setSessions((prev) => [newSession, ...prev])
      setActiveSessionId(newSession.id)
      setMessages([])
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteSession(sessionId) {
    try {
      await chatApi.deleteSession(sessionId)
      const remaining = sessions.filter((s) => s.id !== sessionId)
      setSessions(remaining)
      if (activeSessionId === sessionId) {
        if (remaining.length > 0) {
          loadSession(remaining[0].id)
        } else {
          handleNewChat()
        }
      }
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSendMessage(text) {
    if (!activeSessionId) return
    setError('')

    // Optimistic user message
    const tempUserMsg = { id: `user_${Date.now()}`, role: 'USER', content: text }
    setMessages((prev) => [...prev, tempUserMsg])
    setLoading(true)

    try {
      const responseData = await chatApi.sendMessage(activeSessionId, text)
      const assistantMsg = {
        id: `asst_${Date.now()}`,
        role: 'ASSISTANT',
        content: responseData.message,
        action: responseData.action,
        parameters: responseData.parameters,
        mcqs: responseData.mcqs
      }
      setMessages((prev) => [...prev, assistantMsg])

      // If session title was updated, refresh sessions list
      chatApi.listSessions().then(setSessions).catch(() => {})
    } catch (err) {
      setError(err.message || 'Failed to get response. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  function handleActionNavigation(action, parameters) {
    if (action === 'OPEN_PRACTICE') {
      if (setPracticePrefill) setPracticePrefill(parameters)
      setPage('practice')
    } else if (action === 'OPEN_MOCK_TEST') {
      if (setMockTestPrefill) setMockTestPrefill(parameters)
      setPage('test')
    } else if (action === 'OPEN_REVISION') {
      setPage('revision')
    }
  }

  const activeSession = sessions.find((s) => s.id === activeSessionId)

  return (
    <div className="chat-layout">
      <ChatSidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={loadSession}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
      />

      <ChatWindow
        session={activeSession}
        messages={messages}
        onSendMessage={handleSendMessage}
        onStartAction={handleActionNavigation}
        onEditAction={handleActionNavigation}
        loading={loading}
      />
    </div>
  )
}
