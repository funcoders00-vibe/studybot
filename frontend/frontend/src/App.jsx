import { useEffect, useState } from 'react'
import Sidebar from './Sidebar'
import Dashboard from './Dashboard'
import Practice from './Practice'
import MockTestSetup from './MockTestSetup'
import Test from './Test'
import TestResult from './TestResult'
import Revision from './Revision'
import Progress from './Progress'
import Login from './Login'
import StudyChat from './pages/StudyChat'
import { studybotApi } from './services/api'
import './App.css'

const screens = {
  dashboard: Dashboard,
  study_chat: StudyChat,
  practice: Practice,
  test: MockTestSetup,
  question: Test,
  result: TestResult,
  revision: Revision,
  progress: Progress,
}

export default function App() {
  const [user, setUser] = useState(null)
  const [checking, setChecking] = useState(true)
  const [page, setPage] = useState('dashboard')
  const [practicePrefill, setPracticePrefill] = useState(null)
  const [mockTestPrefill, setMockTestPrefill] = useState(null)
  const [testId, setTestIdState] = useState(() => {
    const saved = localStorage.getItem('studybot_active_test_id')
    return saved ? Number(saved) : null
  })

  function setTestId(id) {
    setTestIdState(id)
    if (id) {
      localStorage.setItem('studybot_active_test_id', String(id))
    } else {
      localStorage.removeItem('studybot_active_test_id')
    }
  }

  useEffect(() => {
    const isExplicitlyLoggedIn = sessionStorage.getItem('studybot_authenticated') === 'true'
    if (!isExplicitlyLoggedIn) {
      setUser(null)
      setChecking(false)
      return
    }

    studybotApi.currentUser()
      .then(({ user: current }) => {
        setUser(current)
        const savedId = localStorage.getItem('studybot_active_test_id')
        if (savedId) {
          studybotApi.getTest(Number(savedId))
            .then((t) => {
              if (t.status === 'IN_PROGRESS') {
                setPage('question')
              }
            })
            .catch(() => {
              localStorage.removeItem('studybot_active_test_id')
              setTestIdState(null)
            })
        }
      })
      .catch(() => {
        sessionStorage.removeItem('studybot_authenticated')
        setUser(null)
      })
      .finally(() => setChecking(false))
  }, [])

  function handleLogin(loggedInUser) {
    sessionStorage.setItem('studybot_authenticated', 'true')
    setUser(loggedInUser)
  }

  // Strict single login screen initial gating
  if (checking) return <main className="loading-page">Loading StudyBot…</main>
  if (!user) return <Login onLogin={handleLogin} />

  const Screen = screens[page] ?? Dashboard

  async function logout() {
    try {
      await studybotApi.logout()
    } catch {
      // Ignore logout errors
    }
    sessionStorage.removeItem('studybot_authenticated')
    setUser(null)
    setPage('dashboard')
    setTestId(null)
    setPracticePrefill(null)
    setMockTestPrefill(null)
  }

  return (
    <div className="shell">
      <Sidebar page={page} setPage={setPage} />
      <div className="area">
        <header>
          <div className="mobile-logo"><i>S</i><b>StudyBot</b></div>
          <label>⌕ <input placeholder="Search topics, notes, formulas…" /></label>
          <div className="profile">
            <button onClick={logout} title="Logout">↪</button>
            <i>{user?.name?.[0]?.toUpperCase() || 'U'}</i>
          </div>
        </header>
        <main>
          <Screen
            setPage={setPage}
            testId={testId}
            setTestId={setTestId}
            user={user}
            prefill={page === 'practice' ? practicePrefill : (page === 'test' ? mockTestPrefill : null)}
            clearPrefill={page === 'practice' ? () => setPracticePrefill(null) : (page === 'test' ? () => setMockTestPrefill(null) : null)}
            setPracticePrefill={setPracticePrefill}
            setMockTestPrefill={setMockTestPrefill}
          />
        </main>
      </div>
    </div>
  )
}
