import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyticsAPI } from '../api'

function StreakTracker() {
  const [channelId, setChannelId] = useState('')
  const [streakData, setStreakData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await analyticsAPI.analyzeUploadStreak(channelId)
      console.log('Streak response:', response.data)
      setStreakData(response.data)
    } catch (err) {
      console.error('Streak analysis error:', err)
      setError(err.response?.data?.error?.message || 'Failed to analyze streak')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <img src="/insight_stream_logo.png" alt="InsightStream" className="logo" />
          <h2>INSIGHTSTREAM</h2>
          <p>Build Awesome</p>
        </div>
        
        <nav className="sidebar-nav">
          <button className="nav-item" onClick={() => navigate('/')}>
            <span className="nav-icon">🏠</span>
            <span>Home</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/thumbnail')}>
            <span className="nav-icon">🎨</span>
            <span>Thumbnail Generator</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/search')}>
            <span className="nav-icon">🔍</span>
            <span>Thumbnail Search</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/hashtags')}>
            <span className="nav-icon">🔑</span>
            <span>Keywords</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/keywords')}>
            <span className="nav-icon">📊</span>
            <span>Keyword Research</span>
          </button>
          <button className="nav-item active" onClick={() => navigate('/streak')}>
            <span className="nav-icon">📈</span>
            <span>Upload Streak</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/content')}>
            <span className="nav-icon">💡</span>
            <span>AI Content Generator</span>
          </button>
          <button className="nav-item" onClick={handleLogout}>
            <span className="nav-icon">🚪</span>
            <span>Logout</span>
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <h1>📊 Upload Streak Tracker</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="streak-hero">
          <p>Track your upload consistency and get AI-powered recommendations</p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleAnalyze} className="streak-form">
          <input
            type="text"
            value={channelId}
            onChange={(e) => setChannelId(e.target.value)}
            placeholder="Enter YouTube Channel URL or @username"
            required
          />
          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Channel'}
          </button>
        </form>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Analyzing upload streak...</p>
          </div>
        )}

        {streakData && !streakData.error && (
          <>
            <div className="channel-banner">
              <div className="channel-info">
                <h3>{streakData.channel_id}</h3>
                <p>Total Videos: {streakData.total_videos}</p>
              </div>
              <button className="btn btn-secondary" onClick={() => setStreakData(null)}>
                Change Channel
              </button>
            </div>

            <div className="algorithm-score-card">
              <h3>YouTube Algorithm Score</h3>
              <div className="score-circle">
                <div className="score-value">{streakData.algorithm_score}</div>
              </div>
              <div className="score-details">
                <p>Based on YouTube's recommendation algorithm:</p>
                <ul>
                  <li>✓ Upload Frequency: {streakData.consistency_metrics?.frequency_score?.toFixed(1) || 0}</li>
                  <li>✓ Consistency: {streakData.consistency_metrics?.consistency_score?.toFixed(1) || 0}%</li>
                  <li>✓ Avg Gap: {streakData.consistency_metrics?.avg_gap_days || 0} days</li>
                </ul>
              </div>
            </div>

            <div className="streak-stats">
              <div className="stat-card">
                <div className="stat-icon">⚡</div>
                <div className="stat-label">Current Streak</div>
                <div className="stat-value">0 days</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📹</div>
                <div className="stat-label">Last 7 Days</div>
                <div className="stat-value">0 videos</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📈</div>
                <div className="stat-label">Last 30 Days</div>
                <div className="stat-value">{streakData.shorts_count + streakData.regular_count} videos</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📅</div>
                <div className="stat-label">Days Since Last</div>
                <div className="stat-value">20 days</div>
              </div>
            </div>

            {streakData.growth_suggestions && streakData.growth_suggestions.length > 0 && (
              <div className="suggestions-section">
                <h3>💡 AI Recommendations</h3>
                <div className="suggestions-list">
                  {streakData.growth_suggestions.map((suggestion, index) => (
                    <div key={index} className="suggestion-card">
                      <p>{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {streakData.upload_schedule && (
              <div className="schedule-section">
                <h3>📅 Recommended Upload Days</h3>
                <div className="schedule-days">
                  {streakData.upload_schedule.recommended_days?.map((day, index) => (
                    <div key={index} className="day-badge">{day}</div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default StreakTracker
