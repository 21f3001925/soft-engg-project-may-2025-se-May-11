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
  try {
    const token = localStorage.getItem('token');
    const headers = {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
    const response = await axios.put(`${API_URL}/accessibility`, settings, {
      headers: headers,
    });
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
