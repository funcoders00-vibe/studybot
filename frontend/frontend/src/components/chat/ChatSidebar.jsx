export default function ChatSidebar({ sessions, activeSessionId, onSelectSession, onNewChat, onDeleteSession }) {
  return (
    <div className="chat-sidebar">
      <div className="chat-sidebar-header">
        <h2>Study Sessions</h2>
        <button className="new-chat-btn" onClick={onNewChat}>
          + New Chat
        </button>
      </div>

      <div className="chat-session-list">
        {sessions.length === 0 ? (
          <p style={{ fontSize: '0.74rem', color: 'var(--muted)', padding: '0.5rem' }}>
            No saved sessions yet.
          </p>
        ) : (
          sessions.map((s) => (
            <div
              key={s.id}
              className={`chat-session-item ${s.id === activeSessionId ? 'active' : ''}`}
              onClick={() => onSelectSession(s.id)}
            >
              <span className="chat-session-title" title={s.title}>
                💬 {s.title}
              </span>
              {onDeleteSession && (
                <button
                  type="button"
                  style={{ background: 'transparent', color: '#9aa0b0', padding: '0.2rem', fontSize: '0.7rem' }}
                  onClick={(e) => {
                    e.stopPropagation()
                    onDeleteSession(s.id)
                  }}
                  title="Delete chat"
                >
                  ✕
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
