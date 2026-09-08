import ChatActionCard from './ChatActionCard'
import StudyContentCard from './StudyContentCard'

export default function ChatMessage({ message, onStartAction, onEditAction }) {
  const isUser = message.role === 'USER'
  const isStudyContent = isUser && message.content?.length > 130

  // Format simple markdown lines (bold, bullet points, headers)
  function renderFormattedContent(text) {
    if (!text) return null
    const lines = text.split('\n')
    return lines.map((line, idx) => {
      if (line.startsWith('### ')) {
        return <h4 key={idx} style={{ margin: '0.6rem 0 0.3rem', fontSize: '0.9rem' }}>{line.replace('### ', '')}</h4>
      }
      if (line.startsWith('## ')) {
        return <h3 key={idx} style={{ margin: '0.7rem 0 0.35rem', fontSize: '1rem' }}>{line.replace('## ', '')}</h3>
      }
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const bulletText = line.substring(2)
        return (
          <p key={idx} style={{ margin: '0.2rem 0', paddingLeft: '0.5rem' }}>
            • {formatBold(bulletText)}
          </p>
        )
      }
      if (line.startsWith('> ')) {
        return (
          <blockquote key={idx} style={{ margin: '0.4rem 0', padding: '0.4rem 0.8rem', background: '#f2f5fc', borderLeft: '3px solid var(--blue)', borderRadius: '0.3rem', fontSize: '0.76rem' }}>
            {formatBold(line.replace('> ', ''))}
          </blockquote>
        )
      }
      if (!line.trim()) {
        return <div key={idx} style={{ height: '0.35rem' }} />
      }
      return <p key={idx} style={{ margin: '0.2rem 0' }}>{formatBold(line)}</p>
    })
  }

  function formatBold(str) {
    const parts = str.split(/(\*\*.*?\*\*)/g)
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <b key={i}>{part.slice(2, -2)}</b>
      }
      if (part.startsWith('*') && part.endsWith('*')) {
        return <em key={i}>{part.slice(1, -1)}</em>
      }
      return part
    })
  }

  return (
    <div className={`chat-msg ${isUser ? 'user' : 'assistant'}`}>
      <div className="chat-msg-avatar">
        {isUser ? 'T' : 'AI'}
      </div>

      <div className="chat-msg-bubble">
        {isStudyContent && (
          <div>
            <span className="study-content-pill">📖 Study Notes Material</span>
          </div>
        )}

        {renderFormattedContent(message.content)}

        {message.mcqs && message.mcqs.length > 0 && (
          <StudyContentCard mcqs={message.mcqs} />
        )}

        {message.action && message.action !== 'NONE' && (
          <ChatActionCard
            action={message.action}
            parameters={message.parameters}
            onStart={onStartAction}
            onEdit={onEditAction}
          />
        )}
      </div>
    </div>
  )
}
