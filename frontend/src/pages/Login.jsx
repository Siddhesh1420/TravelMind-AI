import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Login() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${form.username}&password=${form.password}`
      })
      const data = await res.json()

      if (res.ok) {
        sessionStorage.setItem('token', data.access_token)
        sessionStorage.setItem('username', form.username)
        window.location.href = '/plan'
      } else {
        setError(data.detail || 'Invalid credentials')
      }
    } catch (err) {
      setError('Connection failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6"
      style={{ backgroundColor: '#020817' }}>

      {/* Background */}
      <div className="fixed inset-0 overflow-hidden" style={{ zIndex: 0 }}>
        <img
          src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop"
          alt="" className="w-full h-full object-cover"
          style={{ opacity: 0.2, filter: 'blur(1px)', transform: 'scale(1.05)' }}
        />
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.5) 0%, rgba(2,8,23,0.3) 50%, rgba(2,8,23,0.9) 100%)' }} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md"
        style={{ zIndex: 1 }}>

        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-6">
            <div className="w-2 h-2 rounded-full"
              style={{ backgroundColor: '#2DD4BF', boxShadow: '0 0 8px rgba(45,212,191,0.8)' }} />
            <span style={{ fontFamily: 'Cormorant Garamond', fontSize: '1.2rem', color: '#F1F5F9' }}>
              TravelMind AI
            </span>
          </div>
          <h1 style={{ fontFamily: 'Cormorant Garamond', fontSize: '2.5rem', fontWeight: 400, color: '#F1F5F9' }}>
            Welcome back
          </h1>
          <p className="mt-2" style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter', fontSize: '0.875rem' }}>
            Sign in to plan your next journey
          </p>
        </div>

        {/* Form */}
        <div className="p-8 rounded-2xl"
          style={{ background: 'rgba(15,23,42,0.7)', backdropFilter: 'blur(24px)', border: '1px solid rgba(255,255,255,0.08)' }}>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label style={{ color: 'rgba(100,116,139,0.8)', fontFamily: 'JetBrains Mono', fontSize: '0.65rem', letterSpacing: '0.1em', display: 'block', marginBottom: '0.5rem' }}>
                USERNAME
              </label>
              <input
                type="text"
                placeholder="siddhesh"
                value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })}
                className="w-full px-4 py-3 rounded-xl text-sm outline-none"
                style={{ backgroundColor: 'rgba(15,23,42,0.6)', border: '1px solid rgba(255,255,255,0.08)', color: '#E2E8F0', fontFamily: 'Inter' }}
              />
            </div>

            <div>
              <label style={{ color: 'rgba(100,116,139,0.8)', fontFamily: 'JetBrains Mono', fontSize: '0.65rem', letterSpacing: '0.1em', display: 'block', marginBottom: '0.5rem' }}>
                PASSWORD
              </label>
              <input
                type="password"
                placeholder="••••••••"
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                className="w-full px-4 py-3 rounded-xl text-sm outline-none"
                style={{ backgroundColor: 'rgba(15,23,42,0.6)', border: '1px solid rgba(255,255,255,0.08)', color: '#E2E8F0', fontFamily: 'Inter' }}
              />
            </div>

            {error && (
              <div className="px-4 py-3 rounded-xl text-sm"
                style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', color: 'rgba(252,165,165,0.9)', fontFamily: 'Inter' }}>
                {error}
              </div>
            )}

            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-xl font-medium text-sm transition-all duration-200 hover:opacity-90"
              style={{ background: 'rgba(45,212,191,0.12)', border: '1px solid rgba(45,212,191,0.25)', color: '#2DD4BF', fontFamily: 'Inter' }}>
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center mt-6 text-sm" style={{ color: 'rgba(100,116,139,0.7)', fontFamily: 'Inter' }}>
            No account?{' '}
            <Link to="/register" style={{ color: '#2DD4BF' }}>Create one</Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}