import apiClient from './apiClient';

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
