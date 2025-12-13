import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { thumbnailAPI } from '../api'

function ThumbnailGenerator() {
  const [prompt, setPrompt] = useState('')
  const [thumbnail, setThumbnail] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setThumbnail(null)

    try {
      const response = await thumbnailAPI.generate({ user_input: prompt })
      setThumbnail(response.data.thumbnail_url)
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
    </div>
  )
}

export default ThumbnailGenerator
