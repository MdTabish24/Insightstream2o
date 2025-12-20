import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { keywordAPI } from '../api'

function KeywordResearch() {
  const [query, setQuery] = useState('')
  const [keywords, setKeywords] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleResearch = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await keywordAPI.research({ query })
      console.log('Keywords response:', response.data)
      setKeywords(response.data.keywords || [])
    } catch (err) {
      console.error('Keyword research error:', err)
      setError(err.response?.data?.error?.message || 'Failed to research keywords')
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
          <button className="nav-item active" onClick={() => navigate('/keywords')}>
            <span className="nav-icon">📊</span>
            <span>Keyword Research</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/outlier')}>
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
          <h1>AI Keyword Research</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="keyword-hero">
          <p>Discover trending keywords for your YouTube videos. Get AI-powered keyword suggestions based on real YouTube data.</p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleResearch} className="keyword-form">
          <div className="search-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="How to learn SQL"
              required
            />
            <button type="submit" className="btn-search" disabled={loading}>
              🔍
            </button>
          </div>
        </form>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Researching keywords...</p>
          </div>
        )}

        {keywords.length > 0 && (
          <section className="keywords-section">
            <h3>📈 Primary Keywords</h3>
            <div className="keywords-grid">
              {keywords.map((kw, index) => (
                <div key={index} className="keyword-card">
                  <h4>{kw.keyword || kw}</h4>
                  <div className="keyword-metrics">
                    <span className="metric">Volume: {kw.volume || 'high'}</span>
                    <span className="metric">Competition: {kw.competition || 'high'}</span>
                    <span className="metric">Score: {kw.score || '98'}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default KeywordResearch
