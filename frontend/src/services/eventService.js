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
  getEvents() {
    return apiClient.get('/events');
  },
  getAEvent(event_id) {
    return apiClient.get(`/events/${event_id}`);
  },
  addEvents(eventData) {
    return apiClient.post('/events', eventData);
  },
  updateEvents(event_id, eventData) {
    return apiClient.put(`/events/${event_id}`, eventData);
  },
  deleteEvents(event_id) {
    return apiClient.delete(`/events/${event_id}`);
  },
  joinAEvent() {
    return apiClient.post('/events/join');
  },
};
