import { useNavigate } from 'react-router-dom'

function Dashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  const tools = [
    {
      title: 'AI Thumbnail Generator',
      description: 'Generate professional YouTube thumbnails using AI',
      icon: '🎨',
      image: '/ai_thumbnail_generator.png',
      path: '/thumbnail'
    },
    {
      title: 'AI Search Thumbnail',
      description: 'Search and analyze trending thumbnails',
      icon: '🔍',
      image: '/ai_search_thmbnail.png',
      path: '/analytics'
    },
    {
      title: 'Content Generator',
      description: 'Create engaging video content ideas with AI',
      icon: '📝',
      image: '/content_creation.png',
      path: '/content'
    },
    {
      title: 'Outlier Detection',
      description: 'Identify high and low performing videos',
      icon: '📊',
      image: '/outlier.png',
      path: '/analytics'
    },
    {
      title: 'Trending Hashtags',
      description: 'Discover trending hashtags for your niche',
      icon: '#️⃣',
      image: '/trending hastag.png',
      path: '/hashtags'
    }
  ]

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <img src="/insight_stream_logo.png" alt="InsightStream" className="logo" />
          <h2>INSIGHTSTREAM</h2>
          <p>Build Awesome</p>
        </div>
        
        <nav className="sidebar-nav">
          <button className="nav-item active" onClick={() => navigate('/')}>
            <span className="nav-icon">🏠</span>
            <span>Home</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/thumbnail')}>
            <span className="nav-icon">🎨</span>
            <span>Thumbnail Generator</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/analytics')}>
            <span className="nav-icon">🔍</span>
            <span>Thumbnail Search</span>
          </button>
          <button className="nav-item" onClick={() => navigate('/keywords')}>
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
          <button className="nav-item" onClick={() => navigate('/content')}>
            <span className="nav-icon">💡</span>
            <span>AI Content Generator</span>
          </button>
          <button className="nav-item" onClick={handleLogout}>
            <span className="nav-icon">👤</span>
            <span>Admin</span>
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <h1>5.2 Admin Dashboard</h1>
          <button className="notification-btn">🔔<span className="badge">1</span></button>
        </header>

        <div className="banner">
          <h2>AI Powered YouTube Analytics Tools-Smarter Growth Insights!</h2>
          <p>Unlock the power of your YouTube channel with our cutting-edge, AI-driven analytics platform. We go beyond basic metrics, using artificial intelligence to deliver actionable insights that help you understand what truly drives growth.</p>
        </div>

        <section className="tools-section">
          <h3>AI Tools</h3>
          <div className="tools-grid">
            {tools.map((tool, index) => (
              <div key={index} className="tool-card" onClick={() => navigate(tool.path)}>
                <img src={tool.image} alt={tool.title} />
                <h4>{tool.title}</h4>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default Dashboard
