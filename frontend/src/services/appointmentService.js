// src/services/appointmentService.js
import apiClient from './apiClient';

export default {
  getAppointments(params) {
    return apiClient.get('/appointments', { params }); // Make sure params includes senior_id
  },
  addAppointment(payload) {
    return apiClient.post('/appointments', payload); // Must include senior_id
  },
  updateAppointment(id, payload) {
    return apiClient.put(`/appointments/${id}`, payload);
  },
  deleteAppointment(id) {
    return apiClient.delete(`/appointments/${id}`);
  },
};
