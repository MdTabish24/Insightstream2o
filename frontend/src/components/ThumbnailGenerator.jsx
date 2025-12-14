import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { thumbnailAPI } from '../api'

function ThumbnailGenerator() {
  const [prompt, setPrompt] = useState('')
  const [thumbnail, setThumbnail] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const response = await thumbnailAPI.getHistory()
      setHistory(response.data.results || response.data)
    } catch (err) {
      console.error('Failed to load history:', err)
    }
  }

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setThumbnail(null)

    try {
      const response = await thumbnailAPI.generate({ prompt })
      setThumbnail(response.data.thumbnail_url)
      loadHistory()
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to generate thumbnail')
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
        <h2 style={{ color: '#667eea', marginBottom: '24px' }}>🎨 AI Thumbnail Generator</h2>
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleGenerate}>
          <textarea
            placeholder="Describe your thumbnail (e.g., 'A futuristic city at sunset with neon lights')"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="4"
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Thumbnail'}
          </button>
        </form>

        {thumbnail && (
          <div style={{ marginTop: '24px' }}>
            <h3 style={{ color: '#667eea', marginBottom: '16px' }}>Generated Thumbnail:</h3>
            <img src={thumbnail} alt="Generated thumbnail" className="thumbnail-preview" />
            <button 
              onClick={() => window.open(thumbnail, '_blank')} 
              className="btn btn-secondary"
              style={{ marginTop: '16px', width: '100%' }}
            >
              Download Thumbnail
            </button>
          </div>
        )}
      </div>

      {history.length > 0 && (
        <div className="card" style={{ marginTop: '24px' }}>
          <h2 style={{ color: '#667eea', marginBottom: '24px' }}>📚 Your Thumbnails</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
            {history.map((item) => (
              <div key={item.id} style={{ border: '1px solid #e0e0e0', borderRadius: '8px', padding: '12px' }}>
                <img 
                  src={item.thumbnail_url} 
                  alt={item.prompt} 
                  style={{ width: '100%', borderRadius: '4px', marginBottom: '8px' }}
                />
                <p style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>{item.prompt}</p>
                <p style={{ fontSize: '12px', color: '#999' }}>
                  {new Date(item.created_at).toLocaleDateString()}
                </p>
                <button 
                  onClick={() => window.open(item.thumbnail_url, '_blank')} 
                  className="btn btn-secondary"
                  style={{ marginTop: '8px', width: '100%', padding: '8px' }}
                >
                  Download
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ThumbnailGenerator
