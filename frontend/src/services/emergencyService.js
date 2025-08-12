import apiClient from './apiClient';

export default {
  getEmergencyContacts(seniorId) {
    // If seniorId is provided (for a caregiver), add it as a query param.
    // Otherwise (for a senior), call the base endpoint.
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
