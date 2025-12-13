import axios from 'axios';

const API_BASE_URL = import.meta.env.PROD 
  ? '/api' 
  : 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
          refresh: refreshToken,
        });
        
        localStorage.setItem('access_token', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/users/register/', data),
  login: (data) => api.post('/users/login/', data),
  logout: (refreshToken) => api.post('/users/logout/', { refresh: refreshToken }),
  getProfile: () => api.get('/users/profile/'),
};

export const thumbnailAPI = {
  generate: (data) => api.post('/thumbnails/generate/', data),
  getHistory: () => api.get('/thumbnails/history/'),
};

export const contentAPI = {
  generate: (data) => api.post('/content/generate/', data),
  getHistory: () => api.get('/content/history/'),
};

export const keywordAPI = {
  research: (data) => api.post('/keywords/research/', data),
};

export const hashtagAPI = {
  generate: (data) => api.post('/hashtags/generate/', data),
};

export const analyticsAPI = {
  searchThumbnails: (params) => api.get('/analytics/thumbnail-search/', { params }),
  detectOutliers: (channelId) => api.get('/analytics/outlier/', { params: { channel_id: channelId } }),
  analyzeUploadStreak: (channelId) => api.get('/analytics/upload-streak/', { params: { channel_id: channelId } }),
};

export default api;
