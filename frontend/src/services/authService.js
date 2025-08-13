import apiClient from './apiClient';

export default {
  // Accepts any of: { username, email, phone } and password
  login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },
  signup(payload) {
    return apiClient.post('/auth/signup', payload);
  },
  changePassword(currentPassword, newPassword) {
    return apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_new_password: newPassword, // Backend expects this, though it's validated in frontend
    });
  },
};

class TokenSchema {
  access_token = fields.Str();
  roles = fields.List(fields.Str());
}
