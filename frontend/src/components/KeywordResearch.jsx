import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { keywordAPI } from '../api'

function KeywordResearch() {
  const [topic, setTopic] = useState('')
  const [keywords, setKeywords] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleResearch = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setKeywords(null)

    try {
      const response = await keywordAPI.research({ topic })
      setKeywords(response.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to research keywords')
    } finally {
      setLoading(false)
    }
  }

  const renderKeywords = (keywordList, title) => (
    <div style={{ marginBottom: '24px' }}>
      <h4 style={{ color: '#667eea', marginBottom: '12px' }}>{title}</h4>
      {keywordList.map((item, index) => (
        <div key={index} className="result-card">
          <p><strong>{item.keyword || item.topic}</strong></p>
          <p style={{ fontSize: '14px', marginTop: '4px' }}>
            Search Volume: {item.search_volume} | 
            Competition: {item.competition} | 
            Relevance: {(item.relevance * 100).toFixed(0)}%
          </p>
        </div>
      ))}
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
        <h2 style={{ color: '#667eea', marginBottom: '24px' }}>🔍 Keyword Research</h2>
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleResearch}>
          <input
            type="text"
            placeholder="Enter your topic (e.g., 'Web development')"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Researching...' : 'Research Keywords'}
          </button>
        </form>

        {keywords && (
          <div style={{ marginTop: '24px' }}>
            {renderKeywords(keywords.primary_keywords, '🎯 Primary Keywords')}
            {renderKeywords(keywords.long_tail_keywords, '📊 Long-tail Keywords')}
            {renderKeywords(keywords.trending_keywords, '🔥 Trending Keywords')}
            {renderKeywords(keywords.related_topics, '💡 Related Topics')}
          </div>
        )}
      </div>
    </div>
  )
}

export default KeywordResearch
