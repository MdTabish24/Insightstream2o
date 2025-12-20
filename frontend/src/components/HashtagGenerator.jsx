import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { hashtagAPI } from '../api'

function HashtagGenerator() {
  const [topic, setTopic] = useState('')
  const [hashtags, setHashtags] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await hashtagAPI.generate({ topic })
      console.log('Hashtags response:', response.data)
      // Backend returns combined, real_hashtags, ai_hashtags
      const combined = response.data.combined || response.data.hashtags || []
      setHashtags(combined)
    } catch (err) {
      console.error('Hashtag generation error:', err)
      setError(err.response?.data?.error?.message || 'Failed to generate hashtags')
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
          <button className="nav-item active" onClick={() => navigate('/hashtags')}>
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
          <h1>Trending Hashtags Generator</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        <div className="hashtag-hero">
          <p>Generate trending YouTube hashtags to increase your video reach and engagement.</p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleGenerate} className="hashtag-form">
          <div className="search-input-group">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="How to learn coding"
              required
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              ✨ Generate
            </button>
          </div>
        </form>

        {hashtags.length > 0 && (
          <section className="hashtags-section">
            <h3>📈 Trending Hashtags</h3>
            <div className="hashtags-grid">
              {hashtags.map((tag, index) => (
                <div key={index} className="hashtag-card">
                  <div className="hashtag-title">{tag}</div>
                  <div className="hashtag-badge real">Real YouTube data</div>
                  <div className="hashtag-badge engagement">high</div>
                  <div className="hashtag-badge trending">trending</div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default HashtagGenerator
