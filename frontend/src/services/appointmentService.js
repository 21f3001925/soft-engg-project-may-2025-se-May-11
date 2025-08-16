import apiClient from './apiClient';

export default {
  getAppointments(params = {}) {
    return apiClient.get('/appointments', { params });
  },
  addAppointment(payload) {
    return apiClient.post('/appointments', payload);
  },
  updateAppointment(id, payload) {
    return apiClient.put(`/appointments/${id}`, payload);
  },
  deleteAppointment(id) {
    return apiClient.delete(`/appointments/${id}`);
  },
  completeAppointment(id) {
    return apiClient.patch(`/appointments/${id}`, { status: 'Completed' });
  },
};
