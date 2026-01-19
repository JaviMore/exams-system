import axios from 'axios';

// API base URL comes from Vite env; fall back to dev proxy
const API_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Exams API
export const examsAPI = {
  getAll: () => api.get('/exams/'),
  getById: (id) => api.get(`/exams/${id}`),
  getFullById: (id) => api.get(`/exams/${id}/full`),
  create: (data) => api.post('/exams/', data),
  update: (id, data) => api.put(`/exams/${id}`, data),
  delete: (id) => api.delete(`/exams/${id}`),
};

// Results API
export const resultsAPI = {
  submit: (data) => api.post('/results/', data),
  getMy: () => api.get('/results/my'),
  getById: (id) => api.get(`/results/${id}`),
  getAll: () => api.get('/results/'),
  delete: (id) => api.delete(`/results/${id}`),
};

export default api;
