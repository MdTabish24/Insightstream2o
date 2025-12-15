import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import ThumbnailGenerator from './components/ThumbnailGenerator'
import ThumbnailSearch from './components/ThumbnailSearch'
import ContentGenerator from './components/ContentGenerator'
import KeywordResearch from './components/KeywordResearch'
import HashtagGenerator from './components/HashtagGenerator'
import Analytics from './components/Analytics'
import StreakTracker from './components/StreakTracker'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    setIsAuthenticated(!!token)
  }, [])

  const PrivateRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/login" />
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login setAuth={setIsAuthenticated} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/thumbnail" element={<PrivateRoute><ThumbnailGenerator /></PrivateRoute>} />
        <Route path="/search" element={<PrivateRoute><ThumbnailSearch /></PrivateRoute>} />
        <Route path="/content" element={<PrivateRoute><ContentGenerator /></PrivateRoute>} />
        <Route path="/keywords" element={<PrivateRoute><KeywordResearch /></PrivateRoute>} />
        <Route path="/hashtags" element={<PrivateRoute><HashtagGenerator /></PrivateRoute>} />
        <Route path="/analytics" element={<PrivateRoute><Analytics /></PrivateRoute>} />
        <Route path="/streak" element={<PrivateRoute><StreakTracker /></PrivateRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
