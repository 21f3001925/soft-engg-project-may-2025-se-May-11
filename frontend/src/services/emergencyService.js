import apiClient from './apiClient';

export default {
  // This new function will trigger the alert
  triggerAlert(location) {
    return apiClient.post('/emergency/trigger', location);
  },

  getEmergencyContacts(seniorId) {
    const url = seniorId ? `/emergency-contacts?senior_id=${seniorId}` : '/emergency-contacts';
    return apiClient.get(url);
  },

  addEmergencyContact(contactData, seniorId) {
    const url = seniorId ? `/emergency-contacts?senior_id=${seniorId}` : '/emergency-contacts';
    return apiClient.post(url, contactData);
  },

  updateEmergencyContact(id, contactData, seniorId) {
    const url = seniorId ? `/emergency-contacts/${id}?senior_id=${seniorId}` : `/emergency-contacts/${id}`;
    return apiClient.put(url, contactData);
  },

  deleteEmergencyContact(id, seniorId) {
    const url = seniorId ? `/emergency-contacts/${id}?senior_id=${seniorId}` : `/emergency-contacts/${id}`;
    return apiClient.delete(url);
  },
};
