import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { contentAPI } from '../api'

function ContentGenerator() {
  const [topic, setTopic] = useState('')
  const [concepts, setConcepts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleGenerate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setConcepts([])

    try {
      const response = await contentAPI.generate({ topic })
      setConcepts(response.data.content.concepts)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Failed to generate content')
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
        <h2 style={{ color: '#667eea', marginBottom: '24px' }}>📝 AI Content Generator</h2>
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleGenerate}>
          <input
            type="text"
            placeholder="Enter your video topic (e.g., 'Python programming tutorials')"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Content Ideas'}
          </button>
        </form>

        {concepts.length > 0 && (
          <div style={{ marginTop: '24px' }}>
            <h3 style={{ color: '#667eea', marginBottom: '16px' }}>Generated Concepts:</h3>
            {concepts.map((concept, index) => (
              <div key={index} className="result-card">
                <h4>{concept.title}</h4>
                <p style={{ color: '#667eea', fontWeight: 'bold', marginTop: '8px' }}>
                  SEO Score: {concept.seo_score}/100
                </p>
                <p style={{ marginTop: '12px' }}>
                  <strong>Hook:</strong> {concept.description.hook}
                </p>
                <p style={{ marginTop: '8px' }}>
                  <strong>Main Content:</strong> {concept.description.main_content}
                </p>
                <p style={{ marginTop: '8px' }}>
                  <strong>CTA:</strong> {concept.description.cta}
                </p>
                <p style={{ marginTop: '12px' }}>
                  <strong>Tags:</strong> {concept.tags.join(', ')}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ContentGenerator
