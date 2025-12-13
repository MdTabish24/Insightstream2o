# InsightStream Django API Endpoints

## Authentication Endpoints

### Register
- **POST** `/api/users/register/`
- **Body**: `{"email": "user@example.com", "username": "username", "password": "password123"}`
- **Response**: User data with tokens

### Login
- **POST** `/api/users/login/`
- **Body**: `{"email": "user@example.com", "password": "password123"}`
- **Response**: JWT tokens

### Logout
- **POST** `/api/users/logout/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{"refresh": "refresh_token"}`

### Profile
- **GET** `/api/users/profile/`
- **Headers**: `Authorization: Bearer <access_token>`

### Token Refresh
- **POST** `/api/users/token/refresh/`
- **Body**: `{"refresh": "refresh_token"}`

## AI Thumbnail Generator

### Generate Thumbnail
- **POST** `/api/thumbnails/generate/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{"user_input": "A futuristic city", "ref_image": "optional_url"}`
- **Response**: Generated thumbnail URL

### Thumbnail History
- **GET** `/api/thumbnails/history/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: List of user's thumbnails

## AI Content Generator

### Generate Content
- **POST** `/api/content/generate/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{"topic": "Python programming"}`
- **Response**: 3 video concepts with SEO scores

### Content History
- **GET** `/api/content/history/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: List of user's generated content

## Keyword Research

### Research Keywords
- **POST** `/api/keywords/research/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{"topic": "Web development"}`
- **Response**: Primary, long-tail, trending keywords and related topics

## Trending Hashtags

### Generate Hashtags
- **POST** `/api/hashtags/generate/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{"topic": "Gaming"}`
- **Response**: Real and AI-generated hashtags with engagement metrics

## Analytics

### Thumbnail Search
- **GET** `/api/analytics/thumbnail-search/?query=python+tutorial`
- **GET** `/api/analytics/thumbnail-search/?image_url=https://example.com/image.jpg`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Videos with thumbnails and statistics

### Outlier Detection
- **GET** `/api/analytics/outlier/?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: High and low performing videos using IQR method

### Upload Streak Analysis
- **GET** `/api/analytics/upload-streak/?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Algorithm score, consistency metrics, recommendations

## Admin Dashboard

### Admin Login
- **POST** `/api/admin-dashboard/login/`
- **Body**: `{"username": "admin", "password": "admin_password"}`
- **Response**: Authentication status

### Admin Stats
- **GET** `/api/admin-dashboard/stats/`
- **Note**: Requires admin session from login
- **Response**: Platform statistics, active users, recent registrations

## Error Response Format

All endpoints return errors in this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Common HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - External API error
- `503 Service Unavailable` - AI service unavailable
