export default function ChatActionCard({ action, parameters, onStart, onEdit }) {
  if (!action || action === 'NONE') return null

  const isPractice = action === 'OPEN_PRACTICE'
  const isMock = action === 'OPEN_MOCK_TEST'

  if (!isPractice && !isMock) return null

  const title = isPractice ? 'PRACTICE SESSION' : 'MOCK TEST'
  const icon = isPractice ? '✎' : '◈'

  return (
    <div className="chat-action-card">
      <div className="chat-action-header">
        <b>
          <i>{icon}</i> {title}
        </b>
        <span className="chat-action-badge">Ready to Launch</span>
      </div>

      <div className="chat-action-params">
        <div className="chat-action-param">
          <small>Topic</small>
          <span>{parameters?.custom_topic || parameters?.topic || 'General Studies'}</span>
        </div>

        <div className="chat-action-param">
          <small>Questions</small>
          <span>{parameters?.question_count ?? 10} MCQs</span>
        </div>

        <div className="chat-action-param">
          <small>Difficulty</small>
          <span>{parameters?.difficulty ?? 'MIXED'}</span>
        </div>

        {isMock && (
          <div className="chat-action-param">
            <small>Duration</small>
            <span>{parameters?.duration_minutes ?? 30} Mins</span>
          </div>
        )}

        {parameters?.source === 'CHAT_CONTENT' && (
          <div className="chat-action-param">
            <small>Source</small>
            <span>Chat Content</span>
          </div>
        )}
      </div>

      <div className="chat-action-buttons">
        <button type="button" onClick={() => onEdit(action, parameters)}>
          Edit details
        </button>
        <button
          type="button"
          className="primary"
          onClick={() => onStart(action, parameters)}
        >
          {isPractice ? 'Start Practice →' : 'Start Mock Test →'}
        </button>
      </div>
    </div>
  )
}
