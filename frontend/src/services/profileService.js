import apiClient from './apiClient';

export default {
  getProfile() {
    return apiClient.get('/profile');
  },

  updateProfile(profileData) {
    return apiClient.put('/profile', profileData);
  },

  deleteProfile() {
    return apiClient.delete('/profile');
  },

  changePassword(passwordData) {
    return apiClient.post('/profile/change-password', passwordData);
  },

  uploadAvatar(file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.put('/profile/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};
