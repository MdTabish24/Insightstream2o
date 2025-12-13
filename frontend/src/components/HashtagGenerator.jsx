import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { hashtagAPI } from '../api'

function HashtagGenerator() {
  const [topic, setTopic] = useState('')
  const [hashtags, setHashtags] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setHashtags(null)

    try {
      const response = await hashtagAPI.generate({ topic })
      setHashtags(response.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to generate hashtags')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  const renderHashtagList = (list, title) => (
    <div style={{ marginBottom: '24px' }}>
      <h4 style={{ color: '#667eea', marginBottom: '12px' }}>{title}</h4>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {list.map((item, index) => (
          <div
            key={index}
            onClick={() => copyToClipboard(item.hashtag)}
            style={{
              background: '#f7fafc',
              padding: '8px 16px',
              borderRadius: '20px',
              cursor: 'pointer',
              border: '2px solid #667eea',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => e.target.style.background = '#667eea'}
            onMouseLeave={(e) => e.target.style.background = '#f7fafc'}
          >
            <span style={{ fontWeight: 'bold' }}>{item.hashtag}</span>
            <span style={{ fontSize: '12px', marginLeft: '8px', color: '#666' }}>
              ({item.usage_count})
            </span>
          </div>
        ))}
      </div>
    </div>
  )

  return (
    <div className="container">
      <div className="nav">
        <h1>🎬 InsightStream</h1>
        <button onClick={() => navigate('/')} className="btn btn-secondary">
          Back to Dashboard
        </button>
      </div>

      <div className="card">
        <h2 style={{ color: '#667eea', marginBottom: '24px' }}>#️⃣ Hashtag Generator</h2>
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleGenerate}>
          <input
            type="text"
            placeholder="Enter your topic (e.g., 'Gaming')"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Hashtags'}
          </button>
        </form>

        {hashtags && (
          <div style={{ marginTop: '24px' }}>
            <p style={{ color: '#666', marginBottom: '16px', fontStyle: 'italic' }}>
              Click on any hashtag to copy it!
            </p>
            {renderHashtagList(hashtags.real_hashtags, '🔥 Real Trending Hashtags')}
            {renderHashtagList(hashtags.ai_hashtags, '🤖 AI Generated Hashtags')}
            <div style={{ marginTop: '24px' }}>
              <h4 style={{ color: '#667eea', marginBottom: '12px' }}>📋 All Combined</h4>
              <div className="result-card">
                <p>{hashtags.combined.join(' ')}</p>
                <button
                  onClick={() => copyToClipboard(hashtags.combined.join(' '))}
                  className="btn btn-secondary"
                  style={{ marginTop: '12px' }}
                >
                  Copy All
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default HashtagGenerator
