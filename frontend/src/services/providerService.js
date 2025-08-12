import apiClient from './apiClient';

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
  getEventAttendees(event_id) {
    return apiClient.get(`/events/${event_id}/attendees`);
  },
  removeAttendee(event_id, senior_id) {
    return apiClient.post('/events/unjoin', { event_id, senior_id });
  },
};
