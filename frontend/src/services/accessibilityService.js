import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api/v1';

const getAccessibilitySettings = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${API_URL}/accessibility`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching accessibility settings:', error);
    throw error;
  }
};

const updateAccessibilitySettings = async (settings) => {
  console.log('accessibilityService.js: Sending update request with', settings);
  try {
    const token = localStorage.getItem('token');
    console.log('accessibilityService.js: Retrieved token:', token);
    const headers = {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
    console.log('accessibilityService.js: Request headers:', headers);
    const response = await axios.put(`${API_URL}/accessibility`, settings, {
      headers: headers,
    });
    console.log('accessibilityService.js: Update successful', response.data);
    return response.data;
  } catch (error) {
    console.error('Error updating accessibility settings:', error);
    throw error;
  }
};

export default {
  getAccessibilitySettings,
  updateAccessibilitySettings,
};
