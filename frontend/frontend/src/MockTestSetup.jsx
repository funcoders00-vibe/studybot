import { useEffect, useState } from 'react'
import { studybotApi } from './services/api'

export default function MockTestSetup({ setPage, setTestId, prefill, clearPrefill }) {
  const [topics, setTopics] = useState([])
  const [topicMode, setTopicMode] = useState('PREDEFINED') // 'PREDEFINED' or 'MANUAL'
  const [topicId, setTopicId] = useState('')
  const [customTopic, setCustomTopic] = useState('')
  const [count, setCount] = useState(20)
  const [duration, setDuration] = useState(30)
  const [difficulty, setDifficulty] = useState('MIXED')
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

    if (prefill.chat_session_id) {
      setChatSessionId(prefill.chat_session_id)
    }

    if (prefill.question_count) {
      setCount(Number(prefill.question_count))
    }

    if (prefill.duration_minutes) {
      setDuration(Number(prefill.duration_minutes))
    }

    if (prefill.difficulty) {
      setDifficulty(prefill.difficulty.toUpperCase())
    }

    if (prefill.custom_topic) {
      setTopicMode('MANUAL')
      setCustomTopic(prefill.custom_topic)
    } else if (prefill.topic) {
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
        number_of_questions: Math.max(1, Math.min(Number(count) || 20, 100)),
        duration_minutes: Math.max(1, Math.min(Number(duration) || 30, 180)),
        difficulty,
        chat_session_id: chatSessionId
      }

      if (topicMode === 'PREDEFINED') {
        payload.topic_id = Number(topicId)
      } else {
        payload.custom_topic = customTopic.trim() || 'General Studies'
      }

      const test = await studybotApi.startMockTest(payload)
      setTestId(test.test_id)
      if (clearPrefill) clearPrefill()
      setPage('question')
    } catch (e) {
      setError(e.message || 'Failed to start mock test.')
    } finally {
      setLoading(false)
    }
  }

  const presetCounts = [5, 10, 20, 30, 50, 100]
  const presetDurations = [5, 10, 15, 30, 45, 60, 90, 120]
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
        <i className="setup-icon">◈</i>
        <small>LIVE MOCK TEST</small>
        <h1>Configure mock test</h1>
        <p>
          Timed test with realistic exam conditions. Questions are selected from the syllabus, previous papers, and question bank.
        </p>

        {/* Topic Input Mode Toggle */}
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
                placeholder="e.g. Indian National Movement, General Science, Aptitude..."
                style={{ display: 'block', width: '100%', marginTop: '0.35rem', padding: '0.65rem', borderRadius: '0.55rem', border: '1px solid var(--line)', background: '#fafbff', fontSize: '0.8rem' }}
              />
            </label>
          )}
        </div>

        {/* Question Count Selector */}
        <div style={{ margin: '1.2rem 0', textAlign: 'left' }}>
          <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700', display: 'block', marginBottom: '0.4rem' }}>
            Number of Questions
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

        {/* Duration Selector */}
        <div style={{ margin: '1.2rem 0', textAlign: 'left' }}>
          <label style={{ fontSize: '0.72rem', color: 'var(--muted)', fontWeight: '700', display: 'block', marginBottom: '0.4rem' }}>
            Duration (Minutes)
          </label>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', alignItems: 'center' }}>
            {presetDurations.map((mins) => (
              <button
                key={mins}
                type="button"
                className={duration === mins ? 'primary' : ''}
                style={{ padding: '0.45rem 0.75rem', borderRadius: '0.5rem', fontSize: '0.74rem', fontWeight: '700', background: '#f0f3fa' }}
                onClick={() => setDuration(mins)}
              >
                {mins} mins
              </button>
            ))}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', marginLeft: '0.4rem' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--muted)' }}>Custom:</span>
              <input
                type="number"
                min="1"
                max="180"
                value={duration}
                onChange={(e) => setDuration(Math.max(1, Math.min(180, Number(e.target.value))))}
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
          disabled={loading || (topicMode === 'PREDEFINED' && !topicId) || (topicMode === 'MANUAL' && !customTopic.trim())}
        >
          {loading ? 'Preparing mock test…' : 'Start mock test →'}
        </button>
      </article>
    </section>
  )
}
