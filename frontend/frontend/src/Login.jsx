import { useState } from 'react'
import { studybotApi } from './services/api'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { user } = await studybotApi.login(email.trim(), password)
      onLogin(user)
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  function handleDemoFill() {
    setEmail('')
    setPassword('')
    setError('')
  }

  return (
    <main className="login-wrapper">
      <div className="login-card">
        <div className="login-badge-header">
          <div className="login-brand-icon">
            <span>S</span>
          </div>
          <div className="login-brand-info">
            <h2>StudyBot</h2>
            <span className="login-brand-tag">TNPSC & Exam Sanctuary</span>
          </div>
        </div>

        <div className="login-header-text">
          <h1>Welcome back, Tamil</h1>
          <p>Enter your calm study sanctuary to practice, take mock tests, and review notes.</p>
        </div>

        {error && (
          <div className="login-error-alert" role="alert">
            <span className="error-icon">⚠</span>
            <span>{error}</span>
          </div>
        )}

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-field-group">
            <label htmlFor="login-email">Email Address</label>
            <div className="input-with-icon">
              <span className="input-icon">✉</span>
              <input
                id="login-email"
                type="email"
                required
                autoComplete="email"
                placeholder="tamil@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>

          <div className="login-field-group">
            <div className="field-label-row">
              <label htmlFor="login-password">Password</label>
            </div>
            <div className="input-with-icon">
              <span className="input-icon">🔒</span>
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                required
                autoComplete="current-password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
              <button
                type="button"
                className="toggle-password-btn"
                onClick={() => setShowPassword(!showPassword)}
                title={showPassword ? 'Hide password' : 'Show password'}
                tabIndex={-1}
              >
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="login-submit-btn"
            disabled={loading}
          >
            {loading ? (
              <span className="btn-loading-content">
                <span className="login-spinner"></span>
                <span>Entering Sanctuary…</span>
              </span>
            ) : (
              'Sign In to Study'
            )}
          </button>
        </form>

        <div className="login-divider">
          <span>Quick Demo Access</span>
        </div>

        <button
          type="button"
          className="login-demo-btn"
          onClick={handleDemoFill}
          disabled={loading}
        >
          <span className="demo-icon">⚡</span>
          <span>Fill Demo Account (Tamil)</span>
        </button>

        <div className="login-footer-quote">
          <p>“Calm mind, steady preparation, syllabus-grounded mastery.”</p>
        </div>
      </div>
    </main>
  )
}
