import apiClient from './apiClient';

export default {
  getMedications(seniorId) {
    const url = seniorId ? `/medications?senior_id=${seniorId}` : '/medications';
    return apiClient.get(url);
  },
  addMedication(medicationData, seniorId) {
    const url = seniorId ? `/medications?senior_id=${seniorId}` : '/medications';
    return apiClient.post(url, medicationData);
  },
  updateMedication(id, medicationData, seniorId) {
    const url = seniorId ? `/medications/${id}?senior_id=${seniorId}` : `/medications/${id}`;
    return apiClient.put(url, medicationData);
  },
  deleteMedication(id, seniorId) {
    const url = seniorId ? `/medications/${id}?senior_id=${seniorId}` : `/medications/${id}`;
    return apiClient.delete(url);
  },
};
