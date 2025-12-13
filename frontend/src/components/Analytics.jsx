import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyticsAPI } from '../api'

function Analytics() {
  const [channelId, setChannelId] = useState('')
  const [outliers, setOutliers] = useState(null)
  const [streak, setStreak] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleOutliers = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setOutliers(null)

    try {
      const response = await analyticsAPI.detectOutliers(channelId)
      setOutliers(response.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to detect outliers')
    } finally {
      setLoading(false)
    }
  }

  const handleStreak = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setStreak(null)

    try {
      const response = await analyticsAPI.analyzeUploadStreak(channelId)
      setStreak(response.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to analyze streak')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="nav">
        <h1>🎬 InsightStream</h1>
        <button onClick={() => navigate('/')} className="btn btn-secondary">
          Back to Dashboard
        </button>
      </div>

      <div className="card">
        <h2 style={{ color: '#667eea', marginBottom: '24px' }}>📊 Channel Analytics</h2>
        {error && <div className="error">{error}</div>}
        
        <input
          type="text"
          placeholder="Enter YouTube Channel ID (e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw)"
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
        />

        <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
          <button onClick={handleOutliers} className="btn btn-primary" disabled={loading || !channelId}>
            {loading ? 'Analyzing...' : 'Detect Outliers'}
          </button>
          <button onClick={handleStreak} className="btn btn-secondary" disabled={loading || !channelId}>
            {loading ? 'Analyzing...' : 'Analyze Upload Streak'}
          </button>
        </div>

        {outliers && (
          <div style={{ marginTop: '32px' }}>
            <h3 style={{ color: '#667eea', marginBottom: '16px' }}>🎯 Outlier Detection Results</h3>
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
                      Views: {video.views.toLocaleString()} | 
                      Views/Day: {video.views_per_day.toLocaleString()} | 
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
                      Views: {video.views.toLocaleString()} | 
                      Views/Day: {video.views_per_day.toLocaleString()} | 
                      SmartScore: {video.smart_score}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {streak && (
          <div style={{ marginTop: '32px' }}>
            <h3 style={{ color: '#667eea', marginBottom: '16px' }}>📈 Upload Streak Analysis</h3>
            <div className="stats">
              <div className="stat-item">
                <div className="stat-value">{streak.algorithm_score}</div>
                <div className="stat-label">Algorithm Score</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{streak.total_videos}</div>
                <div className="stat-label">Total Videos</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{streak.consistency_metrics?.avg_gap_days}</div>
                <div className="stat-label">Avg Gap (days)</div>
              </div>
            </div>

            <div style={{ marginTop: '24px' }}>
              <h4 style={{ color: '#667eea', marginBottom: '12px' }}>📅 Recommended Upload Days</h4>
              <div className="result-card">
                <p>{streak.upload_schedule?.recommended_days.join(', ')}</p>
              </div>
            </div>

            {streak.growth_suggestions && (
              <div style={{ marginTop: '24px' }}>
                <h4 style={{ color: '#667eea', marginBottom: '12px' }}>💡 Growth Suggestions</h4>
                {streak.growth_suggestions.map((suggestion, index) => (
                  <div key={index} className="result-card">
                    <p>{suggestion}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Analytics
