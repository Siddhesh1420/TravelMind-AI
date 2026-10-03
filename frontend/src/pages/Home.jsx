import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { DEMO_TRIP } from '../utils/demo'

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#020817' }}>

      {/* Ambient glows */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 w-[600px] h-[600px] rounded-full opacity-8"
          style={{ background: 'radial-gradient(circle, #2DD4BF, transparent)', filter: 'blur(100px)' }} />
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 rounded-full opacity-5"
          style={{ background: 'radial-gradient(circle, #38BDF8, transparent)', filter: 'blur(80px)' }} />
      </div>

      {/* Hero */}
<section className="relative min-h-screen flex items-center justify-center px-6 pt-20">

  {/* Cinematic background */}
  <div className="fixed inset-0 overflow-hidden" style={{ zIndex: 0 }}>
    <img
      src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop"
      alt=""
      className="w-full h-full object-cover"
      style={{ opacity: 0.40, filter: 'blur(1px)', transform: 'scale(1.05)' }}
    />
    <div className="absolute inset-0"
      style={{ background: 'linear-gradient(to bottom, rgba(2,8,23,0.2) 0%, rgba(2,8,23,0.1) 40%, rgba(2,8,23,0.6) 80%, rgba(2,8,23,1) 100%)' }} />
    <div className="absolute inset-0"
      style={{ background: 'radial-gradient(ellipse at 50% 60%, rgba(45,212,191,0.12) 0%, transparent 70%)' }} />
  </div>

  {/* Content */}
  <div className="max-w-5xl mx-auto text-center" style={{ position: 'relative', zIndex: 1 }}>

    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-10"
      style={{ background: 'rgba(45,212,191,0.06)', border: '1px solid rgba(45,212,191,0.15)' }}>
      <div className="w-1.5 h-1.5 rounded-full"
        style={{ backgroundColor: '#2DD4BF', boxShadow: '0 0 6px rgba(45,212,191,0.8)' }} />
      <span style={{ color: 'rgba(45,212,191,0.9)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem', letterSpacing: '0.1em' }}>
        Multi-Agent AI Travel Intelligence
      </span>
    </motion.div>

    <motion.h1
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay: 0.1 }}
      style={{
        fontFamily: 'Cormorant Garamond',
        fontSize: 'clamp(3rem, 8vw, 6rem)',
        fontWeight: 400,
        color: '#F1F5F9',
        lineHeight: 1.05,
        letterSpacing: '-0.02em',
        marginBottom: '1.5rem'
      }}>
      Your next journey,<br />
      <span style={{ color: '#2DD4BF', fontStyle: 'italic' }}>intelligently planned.</span>
    </motion.h1>

    <motion.p
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      className="max-w-2xl mx-auto mb-12"
      style={{ color: 'rgba(148,163,184,0.8)', fontFamily: 'Inter', fontSize: '1.1rem', lineHeight: 1.7 }}>
      TravelMind researches destinations, understands your preferences,
      and builds a personalized itinerary around the way you actually want to travel.
    </motion.p>

    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="flex flex-col sm:flex-row items-center justify-center gap-4">
      <button
        onClick={() => navigate('/plan')}
        className="px-8 py-4 rounded-2xl font-medium text-base transition-all duration-200 hover:opacity-90"
        style={{
          background: 'rgba(45,212,191,0.15)',
          border: '1px solid rgba(45,212,191,0.3)',
          color: '#2DD4BF',
          fontFamily: 'Inter',
          boxShadow: '0 0 30px rgba(45,212,191,0.1)'
        }}>
        Plan My Trip
      </button>
      <button
        onClick={() => navigate('/trip', { state: { tripData: DEMO_TRIP, isDemo: true } })}
        className="px-8 py-4 rounded-2xl font-medium text-base transition-all duration-200"
        style={{
          background: 'rgba(255,255,255,0.04)',
          border: '1px solid rgba(255,255,255,0.08)',
          color: 'rgba(203,213,225,0.8)',
          fontFamily: 'Inter'
        }}>
        See Demo Trip
      </button>
    </motion.div>
  </div>
</section>

      {/* How it works */}
      <section className="relative py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16">
            <h2 style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(2rem, 4vw, 3rem)', fontWeight: 400, color: '#F1F5F9' }}>
              Four agents. One perfect trip.
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { name: 'Orchestrator', desc: 'Coordinates all agents and evaluates output quality', letter: 'O', color: '#2DD4BF' },
              { name: 'Research', desc: 'Searches flights, hotels, weather and destination data', letter: 'R', color: '#38BDF8' },
              { name: 'Planner', desc: 'Builds your personalized day-by-day itinerary', letter: 'P', color: '#F2D6A2' },
              { name: 'Writer', desc: 'Crafts your final journey document and report', letter: 'W', color: '#2DD4BF' },
            ].map((agent, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="p-6 rounded-2xl"
                style={{
                  background: 'rgba(15,23,42,0.6)',
                  backdropFilter: 'blur(24px)',
                  border: '1px solid rgba(255,255,255,0.06)'
                }}>
                <div className="w-9 h-9 rounded-xl flex items-center justify-center mb-4"
                  style={{ background: `${agent.color}15`, border: `1px solid ${agent.color}25` }}>
                  <span style={{ color: agent.color, fontFamily: 'JetBrains Mono', fontSize: '0.75rem', fontWeight: 500 }}>
                    {agent.letter}
                  </span>
                </div>
                <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1rem', color: '#F1F5F9', fontWeight: 500, marginBottom: '0.5rem' }}>
                  {agent.name}
                </p>
                <p style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter', fontSize: '0.8rem', lineHeight: 1.6 }}>
                  {agent.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="relative py-24 px-6"
        style={{ borderTop: '1px solid rgba(255,255,255,0.04)' }}>
        <div className="max-w-5xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
            style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(2rem, 4vw, 3rem)', fontWeight: 400, color: '#F1F5F9' }}>
            Not just a chatbot.
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: 'Real flight & hotel data', desc: 'Live prices from SerpApi — not made-up suggestions.', accent: '#2DD4BF' },
              { title: 'Weather-aware planning', desc: 'Rainy day on Day 3? Indoor activities planned automatically.', accent: '#38BDF8' },
              { title: 'Budget breakdown', desc: 'Every rupee accounted for — transport, hotel, food, activities.', accent: '#F2D6A2' },
              { title: 'WhatsApp confirmation', desc: 'Receive your itinerary on WhatsApp after confirming.', accent: '#2DD4BF' },
              { title: 'Calendar sync', desc: 'Add all trip activities to Google Calendar in one click.', accent: '#38BDF8' },
              { title: 'Direct booking links', desc: 'Pre-filled links to MakeMyTrip, IRCTC, and Booking.com.', accent: '#F2D6A2' },
            ].map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                className="p-6 rounded-2xl"
                style={{
                  background: 'rgba(15,23,42,0.4)',
                  border: '1px solid rgba(255,255,255,0.05)'
                }}>
                <div className="w-0.5 h-6 rounded-full mb-4" style={{ backgroundColor: f.accent }} />
                <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1rem', color: '#F1F5F9', fontWeight: 500, marginBottom: '0.5rem' }}>
                  {f.title}
                </p>
                <p style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter', fontSize: '0.8rem', lineHeight: 1.6 }}>
                  {f.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-24 px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto">
          <h2 style={{ fontFamily: 'Cormorant Garamond', fontSize: 'clamp(2.5rem, 5vw, 4rem)', fontWeight: 400, color: '#F1F5F9', marginBottom: '1.5rem' }}>
            Ready to explore?
          </h2>
          <p style={{ color: 'rgba(148,163,184,0.7)', fontFamily: 'Inter', marginBottom: '2.5rem' }}>
            Tell TravelMind where you want to go and let the agents do the work.
          </p>
          <button
            onClick={() => navigate('/plan')}
            className="px-10 py-4 rounded-2xl font-medium text-base transition-all duration-200 hover:opacity-90"
            style={{
              background: 'rgba(45,212,191,0.15)',
              border: '1px solid rgba(45,212,191,0.3)',
              color: '#2DD4BF',
              fontFamily: 'Inter',
              boxShadow: '0 0 30px rgba(45,212,191,0.1)'
            }}>
            Start Planning
          </button>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 text-center"
        style={{ borderTop: '1px solid rgba(255,255,255,0.04)' }}>
        <p style={{ color: 'rgba(100,116,139,0.6)', fontFamily: 'JetBrains Mono', fontSize: '0.7rem' }}>
          TravelMind AI — LangGraph · FastAPI · React
        </p>
      </footer>

    </div>
  )
}