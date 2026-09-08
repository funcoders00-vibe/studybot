export default function StudyContentCard({ mcqs }) {
  if (!mcqs || mcqs.length === 0) return null

  return (
    <div className="chat-mcq-list">
      {mcqs.map((q, idx) => {
        const correctOpt = q.correct_option?.toUpperCase()
        return (
          <div key={idx} className="chat-mcq-item">
            <div className="chat-mcq-header">
              <span>QUESTION {idx + 1} OF {mcqs.length}</span>
              {q.difficulty && <small>{q.difficulty}</small>}
            </div>

            <div className="chat-mcq-question">
              {q.question}
            </div>

            <div className="chat-mcq-options">
              {['A', 'B', 'C', 'D'].map((key) => {
                const text = q.options?.[key] || ''
                const isCorrect = key === correctOpt
                return (
                  <div key={key} className={`chat-mcq-opt ${isCorrect ? 'correct' : ''}`}>
                    <b>{key}</b>
                    <span>{text}</span>
                  </div>
                )
              })}
            </div>

            {q.explanation && (
              <div className="chat-mcq-explain">
                <b>Explanation</b>
                <p>{q.explanation}</p>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
