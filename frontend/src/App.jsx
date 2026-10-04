import { BrowserRouter, Routes, Route, useLocation,Navigate} from 'react-router-dom'
import { useEffect } from 'react'
import Home from './pages/Home'
import Planner from './pages/Planner'
import Progress from './pages/Progress'
import TripResult from './pages/TripResult'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'


function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])
  return null
}

function ProtectedRoute({ children }) {
  const token = sessionStorage.getItem('token')
  return token ? children : <Navigate to="/login" />
}

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <div className="min-h-screen" style={{ backgroundColor: '#020817' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/plan" element={<ProtectedRoute><Planner /></ProtectedRoute>} />
          <Route path="/planning" element={<ProtectedRoute><Progress /></ProtectedRoute>} />
          <Route path="/trip" element={<ProtectedRoute><TripResult /></ProtectedRoute>} />
          <Route path="/login" element={<Login/>}/>
          <Route path="/register" element={<Register/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App