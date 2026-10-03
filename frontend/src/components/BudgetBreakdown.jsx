import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { motion } from 'framer-motion'

const COLORS = ['#2DD4BF', '#38BDF8', '#F2D6A2', '#94A3B8']

export default function BudgetBreakdown({ breakdown, total }) {
  if (!breakdown) return null

  const data = [
    { name: 'Transport', value: breakdown.transport || 0 },
    { name: 'Hotel', value: breakdown.hotel || 0 },
    { name: 'Food', value: breakdown.food || 0 },
    { name: 'Activities', value: breakdown.activities || 0 },
  ].filter(d => d.value > 0)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="rounded-2xl p-6"
      style={{
        background: 'rgba(15,23,42,0.6)',
        backdropFilter: 'blur(24px)',
        border: '1px solid rgba(255,255,255,0.08)'
      }}>

      <p style={{ fontFamily: 'Cormorant Garamond', fontSize: '1.1rem', color: '#F1F5F9', fontWeight: 500, marginBottom: '1.5rem' }}>
        Budget breakdown
      </p>

      <div className="flex flex-col md:flex-row items-center gap-8">
        <ResponsiveContainer width={180} height={180}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={55} outerRadius={82}
              paddingAngle={3} dataKey="value">
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#0F172A', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', fontFamily: 'Inter' }}
              itemStyle={{ color: '#E2E8F0' }}
              formatter={(value) => [`₹${value.toLocaleString()}`, '']}
            />
          </PieChart>
        </ResponsiveContainer>

        <div className="space-y-3 flex-1 w-full">
          {data.map((item, i) => (
            <div key={i} className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                <span style={{ color: 'rgba(148,163,184,0.8)', fontFamily: 'Inter', fontSize: '0.875rem' }}>
                  {item.name}
                </span>
              </div>
              <span style={{ color: '#E2E8F0', fontFamily: 'JetBrains Mono', fontSize: '0.875rem', fontWeight: 500 }}>
                ₹{item.value.toLocaleString()}
              </span>
            </div>
          ))}
          <div className="pt-3 flex items-center justify-between"
            style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
            <span style={{ color: '#F1F5F9', fontFamily: 'Inter', fontSize: '0.875rem', fontWeight: 500 }}>
              Total
            </span>
            <span style={{ color: '#2DD4BF', fontFamily: 'JetBrains Mono', fontSize: '0.875rem', fontWeight: 600 }}>
              ₹{total?.toLocaleString() || breakdown.total?.toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}