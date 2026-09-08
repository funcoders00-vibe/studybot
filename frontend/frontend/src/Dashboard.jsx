import { useEffect, useState } from 'react'
import { studybotApi } from './services/api'

function Stat({ label, value, icon }) {
  return (
    <article className="card stat">
      <div>
        <span>{label}</span>
        <i>{icon}</i>
      </div>
      <b>{value}</b>
    </article>
  )
}

export default function Dashboard({ setPage, user }) {
  const [overview, setOverview] = useState(null)
  const [topics, setTopics] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([studybotApi.progress(), studybotApi.topicProgress()])
      .then(([stats, rows]) => {
        setOverview(stats)
        setTopics(rows)
      })
      .catch((err) => setError(err.message))
  }, [])

  return (
    <>
      {error && <p className="api-error">Unable to load live data: {error}</p>}
      <section className="card welcome">
        <div>
          <div className="eyebrow"><i />YOUR STUDY SPACE</div>
          <h1>Good morning, {user.name} 👋</h1>
          <p>Live progress from your completed StudyBot tests and AI study sessions.</p>
        </div>
        <div className="actions">
          <button className="primary" onClick={() => setPage('study_chat')}>💬 Study with AI</button>
          <button onClick={() => setPage('practice')}>✎ Practice questions</button>
          <button onClick={() => setPage('test')}>◈ Mock test</button>
          <button className="mint" onClick={() => setPage('revision')}>↻ Revise mistakes</button>
        </div>
      </section>

      <section className="card" style={{ padding: '1.2rem 1.6rem', marginTop: '1.2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', background: 'linear-gradient(135deg, #f0f4ff 0%, #e8f5ee 100%)', border: '1px solid #dbe5f7' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ width: '2.8rem', height: '2.8rem', borderRadius: '50%', background: 'linear-gradient(135deg, #43517d, #375344)', color: '#fff', display: 'grid', placeItems: 'center', fontSize: '1.4rem' }}>
            💬
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--ink)' }}>Need help understanding a topic?</h3>
            <p style={{ margin: '0.2rem 0 0', fontSize: '0.78rem', color: 'var(--muted)' }}>
              Chat with AI for simple explanations, syllabus-grounded notes, or instant MCQ practice from any text.
            </p>
          </div>
        </div>
        <button className="primary" onClick={() => setPage('study_chat')} style={{ whiteSpace: 'nowrap', padding: '0.65rem 1.1rem' }}>
          Open Study Chat →
        </button>
      </section>

      <section className="stats">
        <Stat label="Overall accuracy" value={overview ? `${overview.overall_accuracy}%` : '—'} icon="↗" />
        <Stat label="Questions attempted" value={overview?.total_attempted ?? '—'} icon="✓" />
        <Stat label="Tests completed" value={overview?.tests_completed ?? '—'} icon="◈" />
        <Stat label="Wrong answers" value={overview?.wrong_answers ?? '—'} icon="!" />
      </section>

      <section className="performance">
        <div className="title">
          <div>
            <h2>Topic-wise performance</h2>
            <p>Updated each time you submit a test.</p>
          </div>
          <button className="filter" onClick={() => setPage('progress')}>View progress →</button>
        </div>
        <div className="subjects">
          {topics.length ? (
            topics.map((topic) => (
              <article key={topic.topic_id}>
                <div>
                  <b>{topic.name}</b>
                  <small>{topic.total_attempted} attempted</small>
                </div>
                <strong>{topic.accuracy_percentage}%</strong>
                <p><i style={{ width: `${topic.accuracy_percentage}%` }} /></p>
              </article>
            ))
          ) : (
            <p>No completed tests yet. Start a practice session to create your data.</p>
          )}
        </div>
      </section>
    </>
  )
}
