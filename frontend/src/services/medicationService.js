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
  getMedications() {
    return apiClient.get('/medications');
  },
  addMedication(medicationData) {
    return apiClient.post('/medications', medicationData);
  },
  updateMedication(id, medicationData) {
    return apiClient.put(`/medications/${id}`, medicationData);
  },
  deletemedication(id) {
    return apiClient.delete(`/medications/${id}`);
  },
};
