import { useNavigate } from 'react-router-dom'
import { authAPI } from '../api'

function Dashboard() {
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      await authAPI.logout(refreshToken)
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      navigate('/login')
    }
  }

  const features = [
    {
      title: '🎨 AI Thumbnail Generator',
      description: 'Generate professional thumbnails using AI',
      path: '/thumbnail'
    },
    {
      title: '📝 Content Generator',
      description: 'Create 3 video concepts with SEO scores',
      path: '/content'
    },
    {
      title: '🔍 Keyword Research',
      description: 'Find trending keywords for your videos',
      path: '/keywords'
    },
    {
      title: '#️⃣ Hashtag Generator',
      description: 'Discover trending hashtags',
      path: '/hashtags'
    },
    {
      title: '📊 Analytics',
      description: 'Analyze channel performance and outliers',
      path: '/analytics'
    }
  ]

  return (
    <div className="container">
      <div className="nav">
        <h1>🎬 InsightStream</h1>
        <button onClick={handleLogout} className="btn btn-secondary">
          Logout
        </button>
      </div>

      <div className="card">
        <h2 style={{ color: '#667eea', marginBottom: '16px' }}>Welcome to InsightStream!</h2>
        <p style={{ color: '#666', fontSize: '18px' }}>
          Your AI-powered YouTube analytics and content creation platform
        </p>
      </div>

      <div className="grid">
        {features.map((feature, index) => (
          <div
            key={index}
            className="feature-card"
            onClick={() => navigate(feature.path)}
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard
