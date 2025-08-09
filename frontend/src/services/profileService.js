import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default {
  getProfile() {
    return apiClient.get('/profile');
  },

  updateProfile(profileData) {
    return apiClient.put('/profile', profileData);
  },

  deleteProfile() {
    return apiClient.delete('/profile');
  },

  changePassword(passwordData) {
    return apiClient.post('/profile/change-password', passwordData);
  },

  uploadAvatar(file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.put('/profile/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};
