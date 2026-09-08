import { useState } from 'react'
import { studybotApi } from './services/api'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('tamil@example.com')
  const [password, setPassword] = useState('studybot-local-password')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  async function submit(event) {
    event.preventDefault(); setError(''); setLoading(true)
    try { const { user } = await studybotApi.login(email, password); onLogin(user) }
    catch (err) { setError(err.message) }
    finally { setLoading(false) }
  }
  return <main className="login-page"><form className="card login-card" onSubmit={submit}><i className="setup-icon">S</i><small>PRIVATE STUDY SPACE</small><h1>Welcome back, Tamil</h1><p>Sign in to continue your calm study session.</p><label>Email<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></label><label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>{error && <p className="api-error">{error}</p>}<button className="primary launch" disabled={loading}>{loading ? 'Signing in…' : 'Login to Study'}</button></form></main>
}
