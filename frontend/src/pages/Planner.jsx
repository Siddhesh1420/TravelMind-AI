import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { planTrip } from '../services/api'

const PREFERENCES = ['Budget', 'Luxury', 'Adventure', 'Cultural', 'Vegetarian', 'Family', 'Solo', 'Romantic']
const TRAVEL_MODES = ['train', 'flight', 'car', 'bus']

const inputStyle = {
  backgroundColor: 'rgba(15,23,42,0.6)',
  border: '1px solid rgba(255,255,255,0.08)',
  color: '#E2E8F0',
  backdropFilter: 'blur(12px)',
  fontFamily: 'Inter',
  fontSize: '0.875rem',
  outline: 'none',
  borderRadius: '0.75rem',
  padding: '0.875rem 1rem',
  width: '100%',
  colorScheme: 'dark'
}

const labelStyle = {
  color: 'rgba(100,116,139,0.8)',
  fontFamily: 'JetBrains Mono',
  fontSize: '0.65rem',
  letterSpacing: '0.1em',
  display: 'block',
  marginBottom: '0.5rem'
}

export default function Planner() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    from_city: '',
    destination: '',
    start_date: '',
    end_date: '',
    budget: 15000,
    group_size: 2,
    travel_mode: 'train',
    preferences: [],
    phone_number: '',
    user_id: '',
    departure_time: '06:00',
    arrival_time: '23:00'
  })
  const [error, setError] = useState('')

  const togglePreference = (pref) => {
    const lower = pref.toLowerCase()
    setForm(prev => ({
      ...prev,
      preferences: prev.preferences.includes(lower)
        ? prev.preferences.filter(p => p !== lower)
        : [...prev.preferences, lower]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!form.from_city || !form.destination) return setError('Please enter both departure and destination cities.')
    if (!form.start_date || !form.end_date) return setError('Please select travel dates.')
    if (new Date(form.end_date) <= new Date(form.start_date)) return setError('End date must be after start date.')
    navigate('/planning', { state: { tripInput: form } })
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-6" style={{ backgroundColor: '#020817' }}>

              {/* Cinematic background */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 1 }}>
            <img
                src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2000&auto=format&fit=crop"
                alt=""
                className="w-full h-full object-cover"
                style={{ opacity: 0.35, filter: 'blur(1px)', transform: 'scale(1.05)' }}
            />
            <div className="absolute inset-0"
                style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.15) 0%, rgba(2,8,23,0.1) 50%, rgba(2,8,23,0.6) 100%)' }} />
            </div>

      {/* Ambient glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/3 right-1/4 w-96 h-96 rounded-full opacity-6"
          style={{ background: 'radial-gradient(circle, #2DD4BF, transparent)', filter: 'blur(100px)' }} />
      </div>

      <div className="relative max-w-2xl mx-auto" style={{ zIndex: 1 }}>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-10">
          <h1 style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(2.5rem, 5vw, 3.5rem)', fontWeight: 400, color: '#F1F5F9', lineHeight: 1.1 }}>
            Where are you headed?
          </h1>
          <p className="mt-3" style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter', fontSize: '0.95rem' }}>
            Fill in your trip details and let TravelMind do the research.
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          onSubmit={handleSubmit}
          className="space-y-6">


          {/* From / To */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label style={labelStyle}>FROM</label>
              <input type="text" placeholder="Delhi" value={form.from_city}
                onChange={e => setForm({ ...form, from_city: e.target.value })}
                style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>TO</label>
              <input type="text" placeholder="Manali" value={form.destination}
                onChange={e => setForm({ ...form, destination: e.target.value })}
                style={inputStyle} />
            </div>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label style={labelStyle}>START DATE</label>
              <input type="date" value={form.start_date}
                onChange={e => setForm({ ...form, start_date: e.target.value })}
                style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>END DATE</label>
              <input type="date" value={form.end_date}
                onChange={e => setForm({ ...form, end_date: e.target.value })}
                style={inputStyle} />
            </div>
          </div>

          {/* Budget */}
           <div>
            <label style={labelStyle}>BUDGET (INR)</label>
            <div className="relative mt-1">
                <span className="absolute left-4 top-1/2 transform -translate-y-1/2"
                style={{ color: 'rgba(100,116,139,0.6)', fontFamily: 'JetBrains Mono', fontSize: '0.875rem' }}>
                ₹
                </span>
                <input
                type="number"
                min="2000"
                max="500000"
                step="100"
                value={form.budget}
                onChange={e => {
                    const val = parseInt(e.target.value) || 2000
                    setForm({ ...form, budget: val })
                }}
                className="w-full py-3 pr-4 rounded-xl text-sm outline-none"
                style={{
                    paddingLeft: '2rem',
                    backgroundColor: 'rgba(15,23,42,0.6)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    color: '#E2E8F0',
                    fontFamily: 'JetBrains Mono'
                }}
                />
            </div>
            <input
                type="range"
                min="2000"
                max="500000"
                step="1000"
                value={form.budget}
                onChange={e => setForm({ ...form, budget: parseInt(e.target.value) })}
                className="w-full mt-3"
                style={{ accentColor: '#2DD4BF' }}
            />
            <div className="flex justify-between mt-1">
                <span style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'JetBrains Mono', fontSize: '0.65rem' }}>₹2K</span>
                <span style={{ color: '#2DD4BF', fontFamily: 'JetBrains Mono', fontSize: '0.75rem' }}>
                ₹{form.budget.toLocaleString()}
                </span>
                <span style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'JetBrains Mono', fontSize: '0.65rem' }}>₹5L</span>
            </div>
            </div>

          {/* Group size */}
          <div>
            <label style={labelStyle}>GROUP SIZE</label>
            <input type="number" min="1" max="20" value={form.group_size}
              onChange={e => setForm({ ...form, group_size: parseInt(e.target.value) })}
              style={inputStyle} />
          </div>

          {/* Travel mode */}
          <div>
            <label style={labelStyle}>TRAVEL MODE</label>
            <div className="flex gap-2 mt-1">
              {TRAVEL_MODES.map(mode => (
                <button key={mode} type="button"
                  onClick={() => setForm({ ...form, travel_mode: mode })}
                  className="px-4 py-2 rounded-xl text-sm capitalize transition-all duration-200"
                  style={{
                    background: form.travel_mode === mode ? 'rgba(45,212,191,0.12)' : 'rgba(15,23,42,0.6)',
                    border: form.travel_mode === mode ? '1px solid rgba(45,212,191,0.3)' : '1px solid rgba(255,255,255,0.06)',
                    color: form.travel_mode === mode ? '#2DD4BF' : 'rgba(100,116,139,0.8)',
                    fontFamily: 'Inter',
                    boxShadow: form.travel_mode === mode ? '0 0 12px rgba(45,212,191,0.1)' : 'none'
                  }}>
                  {mode}
                </button>
              ))}
            </div>
          </div>

          {/* Preferences */}
          <div>
            <label style={labelStyle}>PREFERENCES</label>
            <div className="flex flex-wrap gap-2 mt-1">
              {PREFERENCES.map(pref => {
                const isSelected = form.preferences.includes(pref.toLowerCase())
                return (
                  <button key={pref} type="button"
                    onClick={() => togglePreference(pref)}
                    className="px-3 py-1.5 rounded-lg text-sm transition-all duration-200"
                    style={{
                      background: isSelected ? 'rgba(45,212,191,0.1)' : 'rgba(15,23,42,0.6)',
                      border: isSelected ? '1px solid rgba(45,212,191,0.25)' : '1px solid rgba(255,255,255,0.06)',
                      color: isSelected ? '#2DD4BF' : 'rgba(100,116,139,0.7)',
                      fontFamily: 'Inter'
                    }}>
                    {pref}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Time preferences */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label style={labelStyle}>DEPARTURE TIME</label>
              <input type="time" value={form.departure_time}
                onChange={e => setForm({ ...form, departure_time: e.target.value })}
                style={inputStyle} />
              <p className="mt-1" style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'Inter', fontSize: '0.7rem' }}>
                Earliest you want to depart
              </p>
            </div>
            <div>
              <label style={labelStyle}>ARRIVAL TIME</label>
              <input type="time" value={form.arrival_time}
                onChange={e => setForm({ ...form, arrival_time: e.target.value })}
                style={inputStyle} />
              <p className="mt-1" style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'Inter', fontSize: '0.7rem' }}>
                Latest you want to arrive
              </p>
            </div>
          </div>

          {/* WhatsApp */}
          <div>
            <label style={labelStyle}>WHATSAPP (optional)</label>
            <input type="tel" placeholder="+91 98765 43210" value={form.phone_number}
              onChange={e => setForm({ ...form, phone_number: e.target.value })}
              style={inputStyle} />
            <p className="mt-1" style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'Inter', fontSize: '0.7rem' }}>
              Receive your itinerary on WhatsApp
            </p>
          </div>

          {/* Error */}
          {error && (
            <div className="px-4 py-3 rounded-xl text-sm"
              style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', color: 'rgba(252,165,165,0.9)', fontFamily: 'Inter' }}>
              {error}
            </div>
          )}

          {/* Submit */}
          <button type="submit"
            className="w-full py-4 rounded-2xl font-medium text-base transition-all duration-200 hover:opacity-90"
            style={{
              background: 'rgba(45,212,191,0.12)',
              border: '1px solid rgba(45,212,191,0.25)',
              color: '#2DD4BF',
              fontFamily: 'Inter',
              boxShadow: '0 0 30px rgba(45,212,191,0.08)'
            }}>
            Plan My Trip
          </button>

        </motion.form>
      </div>
    </div>
  )
}