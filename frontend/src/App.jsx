import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import Home from './pages/Home'
import Planner from './pages/Planner'
import Progress from './pages/Progress'
import TripResult from './pages/TripResult'
import Navbar from './components/Navbar'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])
  return null
}

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <div className="min-h-screen" style={{ backgroundColor: '#020817' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/plan" element={<Planner />} />
          <Route path="/planning" element={<Progress />} />
          <Route path="/trip" element={<TripResult />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App