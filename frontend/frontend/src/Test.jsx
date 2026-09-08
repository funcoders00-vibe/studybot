import { useEffect, useState } from 'react'
import { studybotApi } from './services/api'

export default function Test({ testId, setPage }) {
  const [questions, setQuestions] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState(() => {
    if (!testId) return {}
    try {
      const saved = localStorage.getItem(`studybot_answers_${testId}`)
      return saved ? JSON.parse(saved) : {}
    } catch {
      return {}
    }
  })
  const [loading, setLoading] = useState(Boolean(testId))
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(!testId ? 'No active test found.' : '')

  useEffect(() => {
    if (!testId) return

    let cancelled = false
    studybotApi.getTest(testId)
      .then((data) => {
        if (cancelled) return
        if (data.status === 'COMPLETED') {
          setPage('result')
          return
        }
        if (!data.questions || data.questions.length === 0) {
          setError('No questions found for this test session.')
          return
        }
        setQuestions(data.questions)
      })
      .catch((err) => {
        if (cancelled) return
        setError(err.message || 'Failed to load test questions.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [testId, setPage])

  function handleSelect(questionId, optionKey) {
    const updated = { ...answers, [questionId]: optionKey }
    setAnswers(updated)
    try {
      localStorage.setItem(`studybot_answers_${testId}`, JSON.stringify(updated))
    } catch {
      // Ignore storage error
    }
  }

  async function handleSubmit() {
    setSubmitting(true)
    setError('')
    try {
      const answerPayload = Object.entries(answers).map(([qid, opt]) => ({
        question_id: Number(qid),
        selected_option: opt,
      }))
      await studybotApi.submitTest(testId, answerPayload)
      try {
        localStorage.removeItem(`studybot_answers_${testId}`)
      } catch {
        // Ignore storage error
      }
      setPage('result')
    } catch (err) {
      setError(err.message || 'Failed to submit test. Please try again.')
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <section className="setup">
        <article className="card">
          <p>Loading questions from question bank…</p>
        </article>
      </section>
    )
  }

  if (error && questions.length === 0) {
    return (
      <section className="setup">
        <article className="card">
          <p className="api-error">{error}</p>
          <div className="actions" style={{ marginTop: '1rem', justifyContent: 'center' }}>
            <button className="primary" onClick={() => setPage('dashboard')}>Return to Dashboard</button>
          </div>
        </article>
      </section>
    )
  }

  const currentQuestion = questions[currentIndex]
  if (!currentQuestion) return null

  const progressPercent = questions.length > 0 ? Math.round(((currentIndex + 1) / questions.length) * 100) : 0
  const selectedOption = answers[currentQuestion.id]

  return (
    <section className="question">
      <div className="test-head">
        <span>QUESTION {currentIndex + 1} OF {questions.length}</span>
        <button onClick={() => setPage('dashboard')}>Leave test</button>
      </div>

      <div className="q-progress">
        <i style={{ width: `${progressPercent}%` }} />
      </div>

      <article className="card">
        <div className="meta">
          <b>QUESTION {currentIndex + 1}</b>
          <small>{currentQuestion.difficulty || 'MEDIUM'}</small>
        </div>

        <h2>{currentQuestion.question_text}</h2>

        <div className="answers">
          {[
            ['A', currentQuestion.option_a],
            ['B', currentQuestion.option_b],
            ['C', currentQuestion.option_c],
            ['D', currentQuestion.option_d],
          ].map(([key, label]) => (
            <button
              key={key}
              type="button"
              className={selectedOption === key ? 'selected' : ''}
              onClick={() => handleSelect(currentQuestion.id, key)}
            >
              <b>{key}</b>
              {label}
            </button>
          ))}
        </div>

        {error && <p className="api-error" style={{ marginTop: '1rem' }}>{error}</p>}

        <div className="footer">
          <button
            type="button"
            disabled={currentIndex === 0 || submitting}
            onClick={() => setCurrentIndex((idx) => Math.max(0, idx - 1))}
          >
            ‹ Previous
          </button>

          {currentIndex < questions.length - 1 ? (
            <button
              type="button"
              className="primary"
              disabled={submitting}
              onClick={() => setCurrentIndex((idx) => Math.min(questions.length - 1, idx + 1))}
            >
              Next question →
            </button>
          ) : (
            <button
              type="button"
              className="primary"
              disabled={submitting}
              onClick={handleSubmit}
            >
              {submitting ? 'Submitting…' : 'Submit test ✓'}
            </button>
          )}
        </div>
      </article>
    </section>
  )
}
