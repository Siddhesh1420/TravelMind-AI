import { useLocation, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { DEMO_TRIP } from '../utils/demo'
import ItineraryCard from '../components/ItineraryCard'
import BudgetBreakdown from '../components/BudgetBreakdown'
import TransportCard from '../components/TransportCard'
import ReactMarkdown from 'react-markdown'

export default function TripResult() {
  const location = useLocation()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('itinerary')

  const tripData = location.state?.tripData
  const isDemo = location.state?.isDemo || false

  // If no state at all (page reload) — go home
  // If isDemo — show demo data
  // If tripData — show real data
  const displayData = tripData || (isDemo ? DEMO_TRIP : null)

  useEffect(() => {
    if (!location.state) {
      navigate('/')
    }
  }, [])

  if (!displayData) return null

  const tabs = [
    { id: 'itinerary', label: 'Itinerary' },
    { id: 'transport', label: 'Transport & Hotel' },
    { id: 'budget', label: 'Budget' },
    { id: 'report', label: 'Full Report' },
  ]

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#020817' }}>

      {/* Cinematic background */}
      <div className="fixed inset-0 overflow-hidden" style={{ zIndex: 0 }}>
        <img
          src="https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2000&auto=format&fit=crop"
          alt=""
          className="w-full h-full object-cover"
          style={{ opacity: 0.30, filter: 'blur(1px)', transform: 'scale(1.05)' }}
        />
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.15) 0%, rgba(2,8,23,0.1) 40%, rgba(2,8,23,0.6) 80%, rgba(2,8,23,0.95) 100%)' }} />
      </div>

      {/* Ambient glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 1 }}>
        <div className="absolute top-0 left-1/3 w-96 h-96 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #2DD4BF, transparent)', filter: 'blur(60px)' }} />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full opacity-6"
          style={{ background: 'radial-gradient(circle, #38BDF8, transparent)', filter: 'blur(80px)' }} />
      </div>

      <div className="relative pt-24 pb-16 px-6" style={{ zIndex: 2 }}>
        <div className="max-w-4xl mx-auto">

          {/* Demo banner */}
          {isDemo && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 px-4 py-3 rounded-xl text-sm text-center"
              style={{ background: 'rgba(242,214,162,0.06)', border: '1px solid rgba(242,214,162,0.2)', color: '#F2D6A2', fontFamily: 'Inter' }}>
              Demo trip to Manali —{' '}
              <button onClick={() => navigate('/plan')} className="underline">plan your own</button>
            </motion.div>
          )}

          {/* Hero Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="mb-10">
            <h1 style={{
              fontFamily: 'Cormorant Garamond',
              fontSize: 'clamp(2.5rem, 6vw, 4rem)',
              fontWeight: 500,
              color: '#F1F5F9',
              lineHeight: 1.1,
              letterSpacing: '-0.01em'
            }}>
              {displayData.from_city} → {displayData.destination}
            </h1>
            <div className="flex flex-wrap items-center gap-3 mt-4">
              <span className="px-3 py-1.5 rounded-lg text-xs"
                style={{ background: 'rgba(45,212,191,0.08)', border: '1px solid rgba(45,212,191,0.2)', color: 'rgba(45,212,191,0.9)', fontFamily: 'JetBrains Mono' }}>
                {displayData.start_date} — {displayData.end_date}
              </span>
              <span className="px-3 py-1.5 rounded-lg text-xs"
                style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', color: 'rgba(148,163,184,0.8)', fontFamily: 'JetBrains Mono' }}>
                {displayData.group_size} {displayData.group_size === 1 ? 'traveller' : 'travellers'}
              </span>
              <span className="px-3 py-1.5 rounded-lg text-xs"
                style={{ background: 'rgba(242,214,162,0.08)', border: '1px solid rgba(242,214,162,0.2)', color: '#F2D6A2', fontFamily: 'JetBrains Mono' }}>
                ₹{displayData.total_estimated_cost?.toLocaleString()} est.
              </span>
            </div>
          </motion.div>

          {/* Glass Tab Bar */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="flex gap-1 mb-8 p-1 rounded-2xl w-fit"
            style={{ background: 'rgba(15,23,42,0.6)', backdropFilter: 'blur(24px)', border: '1px solid rgba(255,255,255,0.06)' }}>
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="px-5 py-2.5 rounded-xl text-sm transition-all duration-200"
                style={{
                  background: activeTab === tab.id ? 'rgba(45,212,191,0.1)' : 'transparent',
                  color: activeTab === tab.id ? '#2DD4BF' : 'rgba(148,163,184,0.7)',
                  border: activeTab === tab.id ? '1px solid rgba(45,212,191,0.2)' : '1px solid transparent',
                  fontFamily: 'Inter',
                  boxShadow: activeTab === tab.id ? '0 0 15px rgba(45,212,191,0.1)' : 'none'
                }}>
                {tab.label}
              </button>
            ))}
          </motion.div>

          {/* Tab Content */}
          {activeTab === 'itinerary' && (
            <div>
              {displayData.itinerary?.map((day, i) => (
                <ItineraryCard
                  key={i}
                  day={day}
                  weather={displayData.weather_data?.[day.date]}
                  index={i}
                />
              ))}
            </div>
          )}

          {activeTab === 'transport' && (
            <TransportCard tripData={displayData} />
          )}

          {activeTab === 'budget' && (
            <BudgetBreakdown
              breakdown={displayData.budget_breakdown}
              total={displayData.total_estimated_cost}
            />
          )}

          {activeTab === 'report' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-2xl p-8 prose prose-invert max-w-none"
              style={{
                background: 'rgba(15,23,42,0.6)',
                backdropFilter: 'blur(24px)',
                border: '1px solid rgba(255,255,255,0.08)',
                color: '#CBD5E1',
                fontFamily: 'Inter'
              }}>
              {displayData.formatted_report
                ? <ReactMarkdown>{displayData.formatted_report}</ReactMarkdown>
                : <p style={{ color: 'rgba(148,163,184,0.6)' }}>No report generated yet.</p>
              }
            </motion.div>
          )}

          {/* Booking Links */}
          {displayData.booking_links && Object.keys(displayData.booking_links).length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mt-8 p-6 rounded-2xl"
              style={{
                background: 'rgba(15,23,42,0.6)',
                backdropFilter: 'blur(24px)',
                border: '1px solid rgba(255,255,255,0.08)'
              }}>
              <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1rem', color: '#F1F5F9', fontWeight: 500, marginBottom: '1rem' }}>
                Book now
              </p>
              <div className="flex flex-wrap gap-3">
                {displayData.booking_links.flight && (
                  <a href={displayData.booking_links.flight} target="_blank" rel="noopener noreferrer"
                    className="px-5 py-2.5 rounded-xl text-sm transition-all duration-200 hover:opacity-90"
                    style={{ background: 'rgba(45,212,191,0.1)', border: '1px solid rgba(45,212,191,0.25)', color: '#2DD4BF', fontFamily: 'Inter' }}>
                    Book flight
                  </a>
                )}
                {displayData.booking_links.train && (
                  <a href={displayData.booking_links.train} target="_blank" rel="noopener noreferrer"
                    className="px-5 py-2.5 rounded-xl text-sm transition-all duration-200 hover:opacity-90"
                    style={{ background: 'rgba(45,212,191,0.1)', border: '1px solid rgba(45,212,191,0.25)', color: '#2DD4BF', fontFamily: 'Inter' }}>
                    Book train
                  </a>
                )}
                {displayData.booking_links.hotel && (
                  <a href={displayData.booking_links.hotel} target="_blank" rel="noopener noreferrer"
                    className="px-5 py-2.5 rounded-xl text-sm transition-all duration-200 hover:opacity-90"
                    style={{ background: 'rgba(56,189,248,0.08)', border: '1px solid rgba(56,189,248,0.2)', color: '#38BDF8', fontFamily: 'Inter' }}>
                    Search hotels
                  </a>
                )}
                {/* Add to Calendar button */}
                {displayData.calendar_events && displayData.calendar_events.length > 0 && (
                <button
                    onClick={async () => {
                    try {
                        // First check if connected
                        const res = await fetch('http://localhost:8000/calendar/create', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            user_id: 'default',
                            calendar_events: displayData.calendar_events
                        })
                        })
                        const data = await res.json()
                        if (res.ok) {
                        alert(`✅ ${data.message}`)
                        } else {
                        // Not connected — redirect to auth
                        const authRes = await fetch('http://localhost:8000/auth/google')
                        const authData = await authRes.json()
                        window.open(authData.auth_url, '_blank')
                        }
                    } catch (err) {
                        alert('Failed to add to calendar. Please try again.')
                    }
                    }}
                    className="px-5 py-2.5 rounded-xl text-sm transition-all duration-200 hover:opacity-90"
                    style={{
                    background: 'rgba(66,133,244,0.1)',
                    border: '1px solid rgba(66,133,244,0.2)',
                    color: '#4285F4',
                    fontFamily: 'Inter'
                    }}>
                    Add to Google Calendar
                </button>
                )}
              </div>
            </motion.div>
          )}

          {/* Action */}
          <div className="mt-8">
            <button
              onClick={() => navigate('/plan')}
              className="px-6 py-3 rounded-xl text-sm transition-all duration-200"
              style={{
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid rgba(255,255,255,0.08)',
                color: 'rgba(148,163,184,0.8)',
                fontFamily: 'Inter'
              }}>
              Plan another trip
            </button>
          </div>

        </div>
      </div>
    </div>
  )
}