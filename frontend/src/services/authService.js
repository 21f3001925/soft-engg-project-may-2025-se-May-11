import apiClient from './apiClient';

export default {
  // Accepts any of: { username, email, phone } and password
  login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },
  signup(payload) {
    return apiClient.post('/auth/signup', payload);
  },
};
