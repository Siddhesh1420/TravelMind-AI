import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { planTrip } from '../services/api'
import { AGENT_STEPS } from '../utils/demo'

export default function Progress() {
  const location = useLocation()
  const navigate = useNavigate()
  const tripInput = location.state?.tripInput

  const [currentStep, setCurrentStep] = useState(0)
  const [status, setStatus] = useState('running')
  const [errorMsg, setErrorMsg] = useState('')

  useEffect(() => {
  if (!tripInput) {navigate('/')  // redirect to home if no state
    return
  }
  runPipeline() }, [])

  const runPipeline = async () => {
    if (!tripInput) return

    let step = 0
    const interval = setInterval(() => {
      step += 1
      if (step < AGENT_STEPS.length - 1) setCurrentStep(step)
      else clearInterval(interval)
    }, 15000)

    try {
      const result = await planTrip(tripInput)
      clearInterval(interval)
      setCurrentStep(AGENT_STEPS.length - 1)
      setStatus('done')
      setTimeout(() => navigate('/trip', { state: { tripData: result } }), 1000)
    } catch (err) {
      clearInterval(interval)
      if (err.code === 'ECONNABORTED') {
            setErrorMsg('Request timed out — but your trip may still be processing. Please check back.')
      } else {
            setErrorMsg(err.response?.data?.detail || 'Something went wrong. Please try again.')
      }
      setStatus('error')
      }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 pt-20"
      style={{ backgroundColor: '#020817' }}>

      {/* Cinematic background */}
    <div className="fixed inset-0 overflow-hidden" style={{ zIndex: 0 }}>
    <img
        src="https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=2000&auto=format&fit=crop"
        alt=""
        className="w-full h-full object-cover"
        style={{ opacity: 0.30, filter: 'blur(1px)', transform: 'scale(1.05)' }}
    />
    <div className="absolute inset-0"
        style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.2) 0%, rgba(2,8,23,0.1) 50%, rgba(2,8,23,0.7) 100%)' }} />
    </div>

      {/* Ambient */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 w-96 h-96 rounded-full opacity-8"
          style={{ background: 'radial-gradient(circle, #2DD4BF, transparent)', filter: 'blur(100px)' }} />
      </div>

      <div className="relative max-w-lg w-full" style={{ zIndex: 1 }}>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12">
          <p style={{ color: 'rgba(45,212,191,0.7)', fontFamily: 'JetBrains Mono', fontSize: '0.65rem', letterSpacing: '0.15em', marginBottom: '0.75rem' }}>
            {status === 'done' ? 'COMPLETE' : status === 'error' ? 'ERROR' : 'PLANNING'}
          </p>
          <h1 style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 400, color: '#F1F5F9' }}>
            {status === 'done'
              ? 'Your trip is ready.'
              : status === 'error'
              ? 'Something went wrong.'
              : `Planning your trip to ${tripInput?.destination}...`}
          </h1>
          {status === 'running' && (
            <p className="mt-3" style={{ color: 'rgba(148,163,184,0.6)', fontFamily: 'Inter', fontSize: '0.875rem' }}>
              This usually takes 1–2 minutes. Our agents are working.
            </p>
          )}
        </motion.div>

        {/* Agent Steps */}
        <div className="space-y-3">
          {AGENT_STEPS.map((step, i) => {
            const isDone = i < currentStep || status === 'done'
            const isActive = i === currentStep && status === 'running'
            const isPending = i > currentStep && status === 'running'

            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: isPending ? 0.35 : 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-center gap-4 p-4 rounded-2xl transition-all duration-500"
                style={{
                  background: isActive ? 'rgba(15,23,42,0.8)' : 'rgba(15,23,42,0.4)',
                  backdropFilter: 'blur(24px)',
                  border: isActive
                    ? '1px solid rgba(45,212,191,0.2)'
                    : isPending
                    ? '1px solid rgba(255,255,255,0.03)'
                    : '1px solid rgba(45,212,191,0.1)',
                  boxShadow: isActive ? '0 0 20px rgba(45,212,191,0.05)' : 'none'
                }}>

                {/* Icon */}
                <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{
                    background: isDone
                      ? 'rgba(45,212,191,0.1)'
                      : isActive
                      ? 'rgba(45,212,191,0.08)'
                      : 'rgba(255,255,255,0.03)',
                    border: isDone || isActive
                      ? '1px solid rgba(45,212,191,0.2)'
                      : '1px solid rgba(255,255,255,0.05)'
                  }}>
                  {isDone
                    ? <span style={{ color: '#2DD4BF', fontSize: '0.75rem' }}>✓</span>
                    : <span style={{ color: isActive ? '#2DD4BF' : 'rgba(100,116,139,0.5)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem', fontWeight: 500 }}>
                        {step.icon}
                      </span>
                  }
                </div>

                {/* Text */}
                <div className="flex-1">
                  <p style={{ color: isDone || isActive ? '#E2E8F0' : 'rgba(100,116,139,0.6)', fontFamily: 'Inter', fontSize: '0.875rem', fontWeight: 500 }}>
                    {step.name}
                  </p>
                  <p style={{ color: 'rgba(100,116,139,0.5)', fontFamily: 'Inter', fontSize: '0.75rem', marginTop: '2px' }}>
                    {step.description}
                  </p>
                </div>

                {/* Pulse */}
                {isActive && (
                  <div className="flex gap-1">
                    {[0, 1, 2].map(dot => (
                      <div key={dot} className="w-1.5 h-1.5 rounded-full"
                        style={{ backgroundColor: '#2DD4BF', animation: `pulse 1.2s ease-in-out ${dot * 0.2}s infinite` }} />
                    ))}
                  </div>
                )}
              </motion.div>
            )
          })}
        </div>

        {/* Error */}
        {status === 'error' && (
          <div className="mt-8 space-y-4">
            <div className="p-4 rounded-xl text-sm"
              style={{ background: 'rgba(239,68,68,0.06)', border: '1px solid rgba(239,68,68,0.15)', color: 'rgba(252,165,165,0.8)', fontFamily: 'Inter' }}>
              {errorMsg}
            </div>
            <button onClick={() => navigate('/plan')}
              className="w-full py-3 rounded-xl text-sm"
              style={{ background: 'rgba(15,23,42,0.6)', border: '1px solid rgba(255,255,255,0.06)', color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter' }}>
              Try Again
            </button>
          </div>
        )}

        <style>{`
          @keyframes pulse {
            0%, 100% { opacity: 0.2; transform: scale(0.7); }
            50% { opacity: 1; transform: scale(1); }
          }
        `}</style>
      </div>
    </div>
  )
}