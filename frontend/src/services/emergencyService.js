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
  getEmergencyContacts() {
    return apiClient.get('/emergency-contacts');
  },
  addEmergencyContact(contactData) {
    return apiClient.post('/emergency-contacts', contactData);
  },
  updateEmergencyContact(id, contactData) {
    return apiClient.put(`/emergency-contacts/${id}`, contactData);
  },
  deleteEmergencyContact(id) {
    return apiClient.delete(`/emergency-contacts/${id}`);
  },
};
