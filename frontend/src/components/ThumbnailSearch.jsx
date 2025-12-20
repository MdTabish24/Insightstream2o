import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyticsAPI } from '../api'

function ThumbnailSearch() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setError('')
    setLoading(true)
    setResults([])

    try {
      const response = await analyticsAPI.searchThumbnails({ query })
      console.log('Search response:', response.data)
      setResults(response.data.results || [])
    } catch (err) {
      console.error('Search error:', err)
      setError(err.response?.data?.error?.message || 'Search failed')
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
          <button className="nav-item active" onClick={() => navigate('/search')}>
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
          <h1>AI Thumbnail Search</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="search-hero">
          <h2>AI Thumbnail Search: Find the Perfect Match Instantly!</h2>
          <p>Turn any video into a high-impact, attention-grabbing thumbnail in seconds! Our AI-powered YouTube thumbnail generator creates professional, eye-catching designs instantly—no design skills needed, just more clicks and views.</p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="jordan peterson on a car"
              required
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              🔍 Search
            </button>
          </div>
        </form>

        {error && <div className="error">{error}</div>}

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Searching for thumbnails...</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="search-results">
            <div className="results-grid">
              {results.map((result, index) => (
                <div key={index} className="result-card-search">
                  <div className="result-thumbnail">
                    <img 
                      src={result.thumbnail_url} 
                      alt={result.title}
                      loading="lazy"
                      onError={(e) => {
                        e.target.src = '/ai_thumbnail_generator.png'
                      }}
                    />
                  </div>
                  <div className="result-info">
                    <h4>{result.title}</h4>
                    <p className="channel-name">{result.channel_title}</p>
                    <div className="result-stats">
                      <span>👁️ {result.views?.toLocaleString() || 0}</span>
                      <span>👍 {result.likes?.toLocaleString() || 0}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {!loading && results.length === 0 && query && (
          <div className="no-results">
            <p>No results found. Try a different search term.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default ThumbnailSearch
