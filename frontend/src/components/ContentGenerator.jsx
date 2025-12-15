import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { contentAPI } from '../api'

function ContentGenerator() {
  const [topic, setTopic] = useState('')
  const [contents, setContents] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await contentAPI.generate({ topic })
      console.log('Content response:', response.data)
      setContents(response.data.content_ideas || [])
    } catch (err) {
      console.error('Content generation error:', err)
      setError(err.response?.data?.error?.message || 'Failed to generate content')
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
          <button className="nav-item" onClick={() => navigate('/analytics')}>
            <span className="nav-icon">📈</span>
            <span>Outlier</span>
          </button>
          <button className="nav-item active" onClick={() => navigate('/content')}>
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
          <h1>AI Content Generator</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="content-hero">
          <p>Generate creative and high-quality content instantly using our AI-powered tool.</p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleGenerate} className="content-form">
          <div className="search-input-group">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Hello world"
              required
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              ✨ Generate
            </button>
          </div>
        </form>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Generating content ideas...</p>
          </div>
        )}

        {contents.length > 0 && (
          <div className="content-results">
            <div className="content-list">
              {contents.map((content, index) => (
                <div key={index} className="content-card">
                  <div className="content-header">
                    <h4>{content.title || `Idea ${index + 1}`}</h4>
                    <button className="copy-btn">📋</button>
                  </div>
                  <p className="content-description">{content.description || content}</p>
                  {content.tags && (
                    <div className="content-tags">
                      {content.tags.map((tag, i) => (
                        <span key={i} className="tag">{tag}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default ContentGenerator
