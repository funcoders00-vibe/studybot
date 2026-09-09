import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'

export default function ChatWindow({
  session,
  messages,
  onSendMessage,
  onStartAction,
  onEditAction,
  loading,
  onToggleSidebar,
}) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="chat-main">
      <div className="chat-header">
        <div className="chat-header-title-wrap">
          <button
            type="button"
            className="mobile-sessions-toggle-btn"
            onClick={onToggleSidebar}
            title="Open study sessions"
            aria-label="Toggle sessions menu"
          >
            ☰ Sessions
          </button>
          <h2>
            <span>💬</span> {session?.title || 'Study Chat'}
          </h2>
        </div>
        <span className="chat-header-subtitle">Grounds questions in your notes & syllabus</span>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            <i>✦</i>
            <h3>Welcome to your AI Study Sanctuary</h3>
            <p>
              Ask any concept question, paste notes, or request multiple choice questions.
              You can turn your conversation into structured practice tests anytime.
            </p>
          </div>
        ) : (
          messages.map((m, idx) => (
            <ChatMessage
              key={m.id || idx}
              message={m}
              onStartAction={onStartAction}
              onEditAction={onEditAction}
            />
          ))
        )}

        {loading && (
          <div className="chat-msg assistant">
            <div className="chat-msg-avatar">AI</div>
            <div className="chat-msg-bubble" style={{ fontStyle: 'italic', color: 'var(--muted)' }}>
              Thinking and reviewing study materials…
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={onSendMessage} disabled={loading} />
    </div>
  )
}
