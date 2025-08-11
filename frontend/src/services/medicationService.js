import apiClient from './apiClient';

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
  deleteMedication(id) {
    return apiClient.delete(`/medications/${id}`);
  },
};
