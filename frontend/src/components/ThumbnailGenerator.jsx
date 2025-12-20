import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { thumbnailAPI } from '../api'

function ThumbnailGenerator() {
  const [prompt, setPrompt] = useState('')
  const [thumbnail, setThumbnail] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const response = await thumbnailAPI.getHistory()
      const data = response.data.results || response.data
      setHistory(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load history:', err)
      setHistory([])
    }
  }

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setThumbnail(null)
    setProgress(0)

    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 2000)

    try {
      const response = await thumbnailAPI.generate({ prompt })
      console.log('Thumbnail response:', response.data)
      const thumbnailUrl = response.data.thumbnail_url
      if (thumbnailUrl) {
        setProgress(100)
        setTimeout(() => {
          setThumbnail(thumbnailUrl)
          loadHistory()
          setPrompt('')
          setProgress(0)
        }, 500)
      } else {
        setError('No thumbnail URL received from server')
      }
    } catch (err) {
      console.error('Thumbnail generation error:', err)
      setError(err.response?.data?.error?.message || err.response?.data?.message || 'Failed to generate thumbnail')
    } finally {
      clearInterval(progressInterval)
      setLoading(false)
    }
  }

  const handleDownload = async (url, filename = 'thumbnail.png') => {
    try {
      const response = await fetch(url)
      const blob = await response.blob()
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    } catch (err) {
      console.error('Download failed:', err)
      window.open(url, '_blank')
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
          <button className="nav-item active" onClick={() => navigate('/thumbnail')}>
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
          <h1>AI Thumbnail Generator</h1>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </header>

        {error && <div className="error">{error}</div>}

        {thumbnail && (
          <div className="generated-thumbnail-card">
            <img 
              src={thumbnail} 
              alt="Generated thumbnail" 
              crossOrigin="anonymous"
              onError={(e) => {
                console.error('Image failed to load:', thumbnail)
                setError('Failed to load generated image.')
                setThumbnail(null)
              }}
            />
            <button 
              className="download-btn"
              onClick={() => handleDownload(thumbnail, `thumbnail_${Date.now()}.png`)}
            >
              ⬇
            </button>
            <p className="thumbnail-prompt">{prompt || 'Generated thumbnail'}</p>
          </div>
        )}

        <form onSubmit={handleGenerate} className="generator-form">
          <textarea
            placeholder="Describe your thumbnail (e.g., 'A futuristic city at sunset with neon lights')"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="4"
            required
            disabled={loading}
          />

          <div className="upload-grid">
            <div className="upload-card disabled">
              <div className="upload-icon">👤</div>
              <h4>Include Face</h4>
              <p>Upload face image</p>
              <span className="coming-soon">Coming Soon</span>
            </div>
            <div className="upload-card disabled">
              <div className="upload-icon">🖼️</div>
              <h4>Reference Image</h4>
              <p>Upload reference image</p>
              <span className="coming-soon">Coming Soon</span>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Thumbnail'}
          </button>

          {loading && (
            <div className="progress-container">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }}></div>
              </div>
              <p className="progress-text">Generating thumbnail... {progress}%</p>
            </div>
          )}
        </form>

        {history.length > 0 && (
          <section className="history-section">
            <h3>Your Generated Thumbnails</h3>
            <div className="history-grid">
              {history.map((item) => (
                <div key={item.id} className="history-card">
                  <img 
                    src={item.thumbnail_url} 
                    alt={item.prompt || item.user_input || 'Thumbnail'} 
                    crossOrigin="anonymous"
                    loading="lazy"
                    onError={(e) => {
                      e.target.style.display = 'none'
                      console.error('History image failed to load:', item.thumbnail_url)
                    }}
                  />
                  <div className="history-info">
                    <p className="history-prompt">{item.prompt || item.user_input || 'No description'}</p>
                    <p className="history-date">{new Date(item.created_at).toLocaleDateString()}</p>
                  </div>
                  <button 
                    className="history-download"
                    onClick={() => handleDownload(item.thumbnail_url, `thumbnail_${item.id}.png`)}
                  >
                    ⬇ Download
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default ThumbnailGenerator
