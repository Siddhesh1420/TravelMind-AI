import { motion } from 'framer-motion'

export default function TransportCard({ tripData }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-4">

      {[
        {
          label: 'Transport',
          content: tripData.recommended_flight_or_train,
          fallback: 'No transport data available',
          accent: '#38BDF8'
        },
        {
          label: 'Hotel',
          content: tripData.recommended_hotel,
          fallback: 'No hotel data available',
          accent: '#2DD4BF'
        }
      ].map(({ label, content, fallback, accent }) => (
        <div key={label} className="rounded-2xl p-6"
          style={{
            background: 'rgba(15,23,42,0.6)',
            backdropFilter: 'blur(24px)',
            border: '1px solid rgba(255,255,255,0.08)'
          }}>
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-4 rounded-full" style={{ backgroundColor: accent }} />
            <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1rem', color: '#F1F5F9', fontWeight: 500 }}>
              {label}
            </p>
          </div>
          <p style={{ color: 'rgba(203,213,225,0.85)', fontFamily: 'Inter', fontSize: '0.875rem', lineHeight: '1.7' }}>
            {content || fallback}
          </p>
          {label === 'Transport' && tripData.transit_note && (
            <div className="mt-3 px-4 py-2.5 rounded-xl text-sm"
              style={{ background: 'rgba(242,214,162,0.06)', border: '1px solid rgba(242,214,162,0.15)', color: '#F2D6A2', fontFamily: 'Inter', fontSize: '0.8rem' }}>
              {tripData.transit_note}
            </div>
          )}
        </div>
      ))}

      {tripData.whatsapp_message && (
        <div className="rounded-2xl p-6"
          style={{
            background: 'rgba(15,23,42,0.6)',
            backdropFilter: 'blur(24px)',
            border: '1px solid rgba(255,255,255,0.08)'
          }}>
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-4 rounded-full" style={{ backgroundColor: '#2DD4BF' }} />
            <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1rem', color: '#F1F5F9', fontWeight: 500 }}>
              WhatsApp summary
            </p>
          </div>
          <pre style={{ color: 'rgba(203,213,225,0.8)', fontFamily: 'Inter', fontSize: '0.8rem', lineHeight: '1.7', whiteSpace: 'pre-wrap' }}>
            {tripData.whatsapp_message}
          </pre>
        </div>
      )}
    </motion.div>
  )
}