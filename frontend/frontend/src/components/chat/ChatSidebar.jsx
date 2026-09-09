export default function ChatSidebar({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  isOpen,
  onClose,
}) {
  return (
    <>
      {isOpen && <div className="chat-sidebar-backdrop" onClick={onClose} />}
      <div className={`chat-sidebar ${isOpen ? 'mobile-open' : ''}`}>
        <div className="chat-sidebar-header">
          <div className="chat-sidebar-title-row">
            <h2>Study Sessions</h2>
            <button
              type="button"
              className="chat-sidebar-close-btn"
              onClick={onClose}
              title="Close sessions list"
              aria-label="Close sessions"
            >
              ✕
            </button>
          </div>
          <button
            className="new-chat-btn"
            onClick={() => {
              onNewChat()
              if (onClose) onClose()
            }}
          >
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
                onClick={() => {
                  onSelectSession(s.id)
                  if (onClose) onClose()
                }}
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
    </>
  )
}
