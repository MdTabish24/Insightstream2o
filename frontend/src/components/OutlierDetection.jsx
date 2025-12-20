import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyticsAPI } from '../api'

function OutlierDetection() {
  const [channelId, setChannelId] = useState('')
  const [outliers, setOutliers] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleDetect = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setOutliers(null)

    try {
      const response = await analyticsAPI.detectOutliers(channelId)
      if (response.data.error) {
        setError(response.data.error)
      } else {
        setOutliers(response.data)
      }
    } catch (err) {
      setError(err.response?.data?.error?.message || err.response?.data?.error || 'Failed to detect outliers')
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
            <span>Hashtags</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/keywords')}>
            <span className="nav-icon">📊</span>
            <span>Keyword Research</span>
          </button>
          <button className="nav-item active" onClick={() => navigate('/outlier')}>
            <span className="nav-icon">📈</span>
            <span>Outlier</span>
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
          <h1>📊 Outlier Detection</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="content-hero">
          <p>Identify your best and worst performing videos using advanced statistical analysis.</p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleDetect} className="content-form">
          <div className="search-input-group">
            <input
              type="text"
              value={channelId}
              onChange={(e) => setChannelId(e.target.value)}
              placeholder="Enter Channel URL or @username (e.g., @MrBeast)"
              required
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Analyzing...' : '🔍 Detect Outliers'}
            </button>
          </div>
        </form>

        {outliers && (
          <div className="outlier-results">
            <div className="stats">
              <div className="stat-item">
                <div className="stat-value">{outliers.total_videos}</div>
                <div className="stat-label">Total Videos</div>
              </div>
              <div className="stat-item">
                <div className="stat-value" style={{ color: '#48bb78' }}>{outliers.high_outliers?.length || 0}</div>
                <div className="stat-label">High Performers</div>
              </div>
              <div className="stat-item">
                <div className="stat-value" style={{ color: '#f56565' }}>{outliers.low_outliers?.length || 0}</div>
                <div className="stat-label">Low Performers</div>
              </div>
            </div>

            {outliers.high_outliers?.length > 0 && (
              <div style={{ marginTop: '24px' }}>
                <h4 style={{ color: '#48bb78', marginBottom: '12px' }}>🚀 Top Performing Videos</h4>
                {outliers.high_outliers.slice(0, 5).map((video, index) => (
                  <div key={index} className="result-card">
                    <h4>{video.title}</h4>
                    <p style={{ marginTop: '8px' }}>
                      Views: {video.views?.toLocaleString()} | 
                      Views/Day: {video.views_per_day?.toLocaleString()} | 
                      SmartScore: {video.smart_score}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {outliers.low_outliers?.length > 0 && (
              <div style={{ marginTop: '24px' }}>
                <h4 style={{ color: '#f56565', marginBottom: '12px' }}>📉 Underperforming Videos</h4>
                {outliers.low_outliers.slice(0, 5).map((video, index) => (
                  <div key={index} className="result-card">
                    <h4>{video.title}</h4>
                    <p style={{ marginTop: '8px' }}>
                      Views: {video.views?.toLocaleString()} | 
                      Views/Day: {video.views_per_day?.toLocaleString()} | 
                      SmartScore: {video.smart_score}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default OutlierDetection
