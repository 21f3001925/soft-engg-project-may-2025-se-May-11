import apiClient from './apiClient';

export default {
  getAssignedSeniors() {
    return apiClient.get('/assignment/my-seniors');
  },
  getAvailableSeniors() {
    return apiClient.get('/assignment/available-seniors');
  },
  assignCaregiverToSenior(senior_id) {
    return apiClient.post('/assignment/assign', { senior_id });
  },
  removeCaregiverFromSenior(senior_id) {
    return apiClient.delete('/assignment/', { data: { senior_id } });
  },
};
