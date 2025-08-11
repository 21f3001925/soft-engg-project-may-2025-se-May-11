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
  getProviders() {
    return apiClient.get('/providers');
  },
  addProvider(providerData) {
    return apiClient.post('/providers', providerData);
  },
  updateProvider(id, providerData) {
    return apiClient.put(`/providers/${id}`, providerData);
  },
  deleteProvider(id) {
    return apiClient.delete(`/providers/${id}`);
  },
  getEvents() {
    return apiClient.get('/events');
  },
  addEvent(eventData) {
    return apiClient.post('/events', eventData);
  },
  updateEvent(id, eventData) {
    return apiClient.put(`/events/${id}`, eventData);
  },
  deleteEvent(id) {
    return apiClient.delete(`/events/${id}`);
  },
};
