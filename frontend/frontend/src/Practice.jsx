import { useEffect, useState } from 'react'
import { studybotApi } from './services/api'

export default function Practice({ setPage, setTestId, prefill, clearPrefill }) {
  const [topics, setTopics] = useState([])
  const [topicMode, setTopicMode] = useState('PREDEFINED') // 'PREDEFINED' or 'MANUAL'
  const [topicId, setTopicId] = useState('')
  const [customTopic, setCustomTopic] = useState('')
  const [count, setCount] = useState(10)
  const [difficulty, setDifficulty] = useState('MIXED')
  const [source, setSource] = useState('DATABASE')
  const [chatSessionId, setChatSessionId] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    studybotApi.topics()
      .then((data) => {
        setTopics(data || [])
        if (!prefill && data && data.length > 0) {
          setTopicId(data[0].id)
        }
      })
      .catch((e) => setError(e.message))
  }, [prefill])

  // Apply prefilled parameters from Chat
  useEffect(() => {
    if (!prefill) return

    if (prefill.source === 'CHAT_CONTENT') {
      setSource('CHAT_CONTENT')
      setChatSessionId(prefill.chat_session_id || null)
    }

    if (prefill.question_count) {
      setCount(Number(prefill.question_count))
    }

    if (prefill.difficulty) {
      setDifficulty(prefill.difficulty.toUpperCase())
    }

    if (prefill.custom_topic) {
      setTopicMode('MANUAL')
      setCustomTopic(prefill.custom_topic)
    } else if (prefill.topic) {
      // Check if matches known topic name
      const matched = topics.find((t) => t.name.toLowerCase() === prefill.topic.toLowerCase())
      if (matched) {
        setTopicMode('PREDEFINED')
        setTopicId(matched.id)
      } else {
        setTopicMode('MANUAL')
        setCustomTopic(prefill.topic)
      }
    }
  }, [prefill, topics])

  async function start() {
    setLoading(true)
    setError('')
    try {
      const payload = {
        number_of_questions: Math.max(1, Math.min(Number(count) || 10, 100)),
        difficulty,
        source,
        chat_session_id: chatSessionId
      }

      if (topicMode === 'PREDEFINED') {
        payload.topic_id = Number(topicId)
      } else {
        payload.custom_topic = customTopic.trim() || 'General Studies'
      }

      const test = await studybotApi.startPractice(payload)
      setTestId(test.test_id)
      if (clearPrefill) clearPrefill()
      setPage('question')
    } catch (e) {
      setError(e.message || 'Failed to start practice test.')
    } finally {
      setLoading(false)
    }
  }

  const presetCounts = [5, 10, 20, 30, 50]
  const difficulties = ['MIXED', 'EASY', 'MEDIUM', 'HARD']

  return (
    <section className="setup">
      <div className="back">
        ‹ <button onClick={() => setPage('dashboard')}>Back to dashboard</button>
        {chatSessionId && (
          <button style={{ marginLeft: '1rem' }} onClick={() => setPage('study_chat')}>
            ‹ Return to Study Chat
          </button>
        )}
      </div>

      <article className="card">
        <i className="setup-icon">✎</i>
        <small>PRACTICE QUESTIONS</small>
        <h1>Configure practice session</h1>
        <p>
          Questions are retrieved from your question bank or generated strictly from syllabus and chat content.
        </p>

        {source === 'CHAT_CONTENT' && (
          <div style={{ margin: '1rem auto', display: 'inline-block', background: '#eaf3ed', color: 'var(--inkmint)', padding: '0.35rem 0.85rem', borderRadius: '999px', fontSize: '0.74rem', fontWeight: '700' }}>
            📖 Sourced directly from your conversation notes
          </div>
        )}

        {/* Topic Input Selector */}
        <div style={{ margin: '1.5rem 0 0.5rem', textAlign: 'left' }}>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.6rem' }}>
            <button
              type="button"
              className={topicMode === 'PREDEFINED' ? 'primary' : ''}
              style={{ padding: '0.4rem 0.75rem', borderRadius: '0.5rem', fontSize: '0.74rem', fontWeight: '700' }}
              onClick={() => setTopicMode('PREDEFINED')}
            >
              Select Predefined Topic
            </button>
            <button
              type="button"
              className={topicMode === 'MANUAL' ? 'primary' : ''}
              style={{ padding: '0.4rem 0.75rem', borderRadius: '0.5rem', fontSize: '0.74rem', fontWeight: '700' }}
              onClick={() => setTopicMode('MANUAL')}
            >
              Enter Topic Manually
            </button>
          </div>

          {topicMode === 'PREDEFINED' ? (
            <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700' }}>
              Choose Topic
              <select
                value={topicId}
                onChange={(e) => setTopicId(e.target.value)}
                style={{ display: 'block', width: '100%', marginTop: '0.35rem', padding: '0.65rem', borderRadius: '0.55rem', border: '1px solid var(--line)', background: '#fafbff' }}
              >
                {topics.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </label>
          ) : (
            <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700' }}>
              Enter Topic Name
              <input
                type="text"
                value={customTopic}
                onChange={(e) => setCustomTopic(e.target.value)}
                placeholder="e.g. Fundamental Rights, Directive Principles, Indus Valley..."
                style={{ display: 'block', width: '100%', marginTop: '0.35rem', padding: '0.65rem', borderRadius: '0.55rem', border: '1px solid var(--line)', background: '#fafbff', fontSize: '0.8rem' }}
              />
            </label>
          )}
        </div>

        {/* Question Count Selector */}
        <div style={{ margin: '1.2rem 0', textAlign: 'left' }}>
          <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700', display: 'block', marginBottom: '0.4rem' }}>
            Question Count
          </label>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', alignItems: 'center' }}>
            {presetCounts.map((num) => (
              <button
                key={num}
                type="button"
                className={count === num ? 'primary' : ''}
                style={{ padding: '0.45rem 0.75rem', borderRadius: '0.5rem', fontSize: '0.74rem', fontWeight: '700', background: '#f0f3fa' }}
                onClick={() => setCount(num)}
              >
                {num} Qs
              </button>
            ))}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', marginLeft: '0.4rem' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--muted)' }}>Custom:</span>
              <input
                type="number"
                min="1"
                max="100"
                value={count}
                onChange={(e) => setCount(Math.max(1, Math.min(100, Number(e.target.value))))}
                style={{ width: '4rem', padding: '0.4rem', borderRadius: '0.4rem', border: '1px solid var(--line)', fontSize: '0.75rem', textAlign: 'center' }}
              />
            </div>
          </div>
        </div>

        {/* Difficulty Selector */}
        <div style={{ margin: '1.2rem 0 1.8rem', textAlign: 'left' }}>
          <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700', display: 'block', marginBottom: '0.4rem' }}>
            Difficulty
          </label>
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            {difficulties.map((diff) => (
              <button
                key={diff}
                type="button"
                className={difficulty === diff ? 'primary' : ''}
                style={{ padding: '0.45rem 0.8rem', borderRadius: '0.5rem', fontSize: '0.74rem', fontWeight: '700', background: '#f0f3fa' }}
                onClick={() => setDifficulty(diff)}
              >
                {diff}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="api-error" style={{ marginBottom: '1rem' }}>{error}</p>}

        <button
          className="primary launch"
          onClick={start}
          disabled={loading || (topicMode === 'PREDEFINED' && !topicId) || (topicMode === 'MANUAL' && !customTopic.trim() && source !== 'CHAT_CONTENT')}
        >
          {loading ? 'Preparing questions…' : 'Start practice →'}
        </button>
      </article>
    </section>
  )
}
