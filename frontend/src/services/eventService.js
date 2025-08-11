import apiClient from './apiClient';

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
  joinAEvent(event_id) {
    return apiClient.post('/events/join', { event_id });
  },
  getJoinedEvents() {
    return apiClient.get('/events/joined');
  },
};
