import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function TripHistory() {
  const navigate = useNavigate()
  const [trips, setTrips] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const token = sessionStorage.getItem('token')
      const res = await fetch('http://localhost:8000/trips/history', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await res.json()
      setTrips(data.trips || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const viewTrip = async (index) => {
    try {
      const token = sessionStorage.getItem('token')
      const res = await fetch(`http://localhost:8000/trips/history/${index}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const tripData = await res.json()
      navigate('/trip', { state: { tripData } })
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-6" style={{ backgroundColor: '#020817' }}>

      {/* Background */}
      <div className="fixed inset-0 overflow-hidden" style={{ zIndex: 0 }}>
        <img
          src="https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2000&auto=format&fit=crop"
          alt="" className="w-full h-full object-cover"
          style={{ opacity: 0.20, filter: 'blur(1px)', transform: 'scale(1.05)' }}
        />
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.3) 0%, rgba(2,8,23,0.8) 100%)' }} />
      </div>

      <div className="relative max-w-4xl mx-auto" style={{ zIndex: 1 }}>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <p className="text-xs mb-2" style={{ color: '#2DD4BF', fontFamily: 'JetBrains Mono', letterSpacing: '0.15em' }}>
            YOUR JOURNEYS
          </p>
          <h1 style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(2.5rem, 5vw, 3.5rem)', fontWeight: 400, color: '#F1F5F9' }}>
            Trip History
          </h1>
        </motion.div>

        {loading ? (
          <p style={{ color: 'rgba(148,163,184,0.6)', fontFamily: 'Inter' }}>Loading...</p>
        ) : trips.length === 0 ? (
          <div className="text-center py-20">
            <p style={{ color: 'rgba(148,163,184,0.6)', fontFamily: 'Inter', marginBottom: '1.5rem' }}>
              No trips yet. Plan your first journey!
            </p>
            <button onClick={() => navigate('/plan')}
              className="px-6 py-3 rounded-xl text-sm"
              style={{ background: 'rgba(45,212,191,0.1)', border: '1px solid rgba(45,212,191,0.2)', color: '#2DD4BF', fontFamily: 'Inter' }}>
              Plan a Trip
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {trips.map((trip, i) => (
              <motion.div key={i}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="p-6 rounded-2xl flex items-center justify-between"
                style={{ background: 'rgba(15,23,42,0.6)', backdropFilter: 'blur(24px)', border: '1px solid rgba(255,255,255,0.08)' }}>

                <div>
                  <h3 style={{ fontFamily: 'Cormorant Garamond', fontSize: '1.3rem', color: '#F1F5F9', fontWeight: 500 }}>
                    {trip.from_city} → {trip.destination}
                  </h3>
                  <div className="flex gap-4 mt-2">
                    <span style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem' }}>
                      {trip.start_date} — {trip.end_date}
                    </span>
                    <span style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem' }}>
                      {trip.travel_mode}
                    </span>
                    <span style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem' }}>
                      {trip.group_size} {trip.group_size === 1 ? 'person' : 'people'}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p style={{ color: '#F2D6A2', fontFamily: 'JetBrains Mono', fontSize: '0.875rem', fontWeight: 500 }}>
                      ₹{trip.total_cost?.toLocaleString()}
                    </p>
                    <p style={{ color: 'rgba(148,163,184,0.5)', fontFamily: 'Inter', fontSize: '0.75rem' }}>
                      of ₹{trip.budget?.toLocaleString()}
                    </p>
                  </div>
                  <button
                    onClick={() => viewTrip(trip.index)}
                    className="px-4 py-2 rounded-xl text-sm transition-all hover:opacity-90"
                    style={{ background: 'rgba(45,212,191,0.1)', border: '1px solid rgba(45,212,191,0.2)', color: '#2DD4BF', fontFamily: 'Inter' }}>
                    View Trip
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}