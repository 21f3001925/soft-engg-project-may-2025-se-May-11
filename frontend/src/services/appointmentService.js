// src/services/appointmentService.js
import apiClient from './apiClient';

export default {
  // Fetch all appointments
  getAppointments() {
    return apiClient.get('/appointments');
  },

  // Add new appointment
  addAppointment(appointmentData) {
    return apiClient.post('/appointments', appointmentData);
  },

  // Update existing appointment
  updateAppointment(appointmentId, appointmentData) {
    return apiClient.put(`/appointments/${appointmentId}`, appointmentData);
  },

  // Delete appointment
  deleteAppointment(appointmentId) {
    return apiClient.delete(`/appointments/${appointmentId}`);
  },
};
