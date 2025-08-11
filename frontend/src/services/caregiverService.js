import apiClient from './apiClient';

export default {
  getAssignedSeniors() {
    return apiClient.get('/profile/caregiver/seniors');
  },
};
