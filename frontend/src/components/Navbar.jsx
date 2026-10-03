import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Navbar() {
  const location = useLocation()

  return (
    <motion.nav
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 left-0 right-0 z-50 px-6 py-5">

      {/* Glass pill container */}
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between px-6 py-3 rounded-2xl"
          style={{
            background: 'rgba(2, 8, 23, 0.5)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255,255,255,0.07)',
            boxShadow: '0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05)'
          }}>

          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5">
            <div className="relative">
              <div className="w-2 h-2 rounded-full"
                style={{ backgroundColor: '#2DD4BF' }} />
              <div className="absolute inset-0 w-2 h-2 rounded-full animate-ping"
                style={{ backgroundColor: '#2DD4BF', opacity: 0.3 }} />
            </div>
            <span style={{
              fontFamily: 'Cormorant Garamond',
              fontSize: '1.15rem',
              fontWeight: 500,
              color: '#F1F5F9',
              letterSpacing: '0.01em'
            }}>
              TravelMind <span style={{ color: 'rgba(45,212,191,0.8)' }}>AI</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="hidden md:flex items-center gap-1">
            {[
              { label: 'Discover', path: '/' },
              { label: 'Plan', path: '/plan' }
            ].map(({ label, path }) => (
              <Link key={path} to={path}
                className="px-4 py-2 rounded-xl text-sm transition-all duration-200"
                style={{
                  color: location.pathname === path
                    ? '#2DD4BF'
                    : 'rgba(148,163,184,0.7)',
                  background: location.pathname === path
                    ? 'rgba(45,212,191,0.08)'
                    : 'transparent',
                  fontFamily: 'Inter'
                }}>
                {label}
              </Link>
            ))}
          </div>

          {/* CTA */}
          <Link to="/plan"
            className="px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200 hover:opacity-90"
            style={{
              background: 'rgba(45,212,191,0.12)',
              border: '1px solid rgba(45,212,191,0.2)',
              color: '#2DD4BF',
              fontFamily: 'Inter',
              boxShadow: '0 0 20px rgba(45,212,191,0.08)'
            }}>
            Plan a Trip
          </Link>
        </div>
      </div>
    </motion.nav>
  )
}