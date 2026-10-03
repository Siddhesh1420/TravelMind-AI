import { motion } from 'framer-motion'

const timeColors = {
  morning: { color: '#F59E0B', label: 'Morning' },
  afternoon: { color: '#38BDF8', label: 'Afternoon' },
  evening: { color: '#2DD4BF', label: 'Evening' }
}

const weatherBg = {
  'clear': 'rgba(251,191,36,0.1)',
  'sunny': 'rgba(251,191,36,0.1)',
  'partly cloudy': 'rgba(148,163,184,0.1)',
  'cloudy': 'rgba(100,116,139,0.1)',
  'light rain': 'rgba(56,189,248,0.1)',
  'moderate rain': 'rgba(56,189,248,0.1)',
  'overcast clouds': 'rgba(100,116,139,0.1)',
  'broken clouds': 'rgba(148,163,184,0.1)',
}

export default function ItineraryCard({ day, weather, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: [0.22, 1, 0.36, 1] }}
      className="relative flex gap-6"
    >
      {/* Timeline */}
      <div className="flex flex-col items-center flex-shrink-0">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center z-10"
          style={{
            background: 'rgba(45,212,191,0.1)',
            border: '1px solid rgba(45,212,191,0.25)',
            boxShadow: '0 0 15px rgba(45,212,191,0.15)'
          }}>
          <span style={{ color: '#2DD4BF', fontFamily: 'JetBrains Mono', fontSize: '0.75rem', fontWeight: 500 }}>
            {day.day_number}
          </span>
        </div>
        {/* Vertical line */}
        <div className="w-px flex-1 mt-2"
          style={{ background: 'linear-gradient(to bottom, rgba(45,212,191,0.3), transparent)' }} />
      </div>

      {/* Card */}
      <div className="flex-1 mb-6 rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.005]"
        style={{
          background: 'rgba(15,23,42,0.6)',
          backdropFilter: 'blur(24px)',
          border: '1px solid rgba(255,255,255,0.08)',
        }}>

        {/* Card Header */}
        <div className="flex items-center justify-between px-6 py-4"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <div>
            <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1.1rem', color: '#F1F5F9', fontWeight: 500 }}>
              Day {day.day_number}
            </p>
            <p style={{ fontFamily: 'JetBrains Mono', fontSize: '0.7rem', color: 'rgba(148,163,184,0.7)', marginTop: '2px' }}>
              {day.date}
            </p>
          </div>

          <div className="flex items-center gap-3">
            {weather && (
              <div className="px-3 py-1.5 rounded-lg"
                style={{
                  background: weatherBg[weather.condition?.toLowerCase()] || 'rgba(148,163,184,0.08)',
                  border: '1px solid rgba(255,255,255,0.06)'
                }}>
                <p style={{ fontFamily: 'JetBrains Mono', fontSize: '0.7rem', color: 'rgba(226,232,240,0.8)' }}>
                  {weather.temp}°C · {weather.condition}
                </p>
              </div>
            )}
            <div className="px-3 py-1.5 rounded-lg"
              style={{ background: 'rgba(242,214,162,0.08)', border: '1px solid rgba(242,214,162,0.15)' }}>
              <p style={{ fontFamily: 'JetBrains Mono', fontSize: '0.7rem', color: '#F2D6A2' }}>
                ₹{day.estimated_cost?.toLocaleString() || '—'}
              </p>
            </div>
          </div>
        </div>

        {/* Activities */}
        <div className="px-6 py-5 space-y-4">
          {(['morning', 'afternoon', 'evening']).map(time => {
            const { color, label } = timeColors[time]
            return (
              <div key={time} className="flex gap-4">
                <div className="w-0.5 rounded-full flex-shrink-0 mt-1"
                  style={{ backgroundColor: color, minHeight: '16px', boxShadow: `0 0 6px ${color}60` }} />
                <div>
                  <p style={{ color, fontFamily: 'JetBrains Mono', fontSize: '0.65rem', fontWeight: 500, marginBottom: '3px', letterSpacing: '0.08em' }}>
                    {label}
                  </p>
                  <p style={{ color: 'rgba(203,213,225,0.85)', fontFamily: 'Inter', fontSize: '0.875rem', lineHeight: '1.6' }}>
                    {day[time] || '—'}
                  </p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </motion.div>
  )
}