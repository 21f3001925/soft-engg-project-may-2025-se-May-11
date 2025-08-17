import axios from 'axios';

const API_URL = 'http://localhost:5001/api/voice-assistant';

const sendVoiceQuery = (audioBlob) => {
  const token = localStorage.getItem('token');
  return axios.post(`${API_URL}/query`, audioBlob, {
    headers: {
      'Content-Type': audioBlob.type || 'audio/webm', // Set appropriate content type
      Authorization: `Bearer ${token}`,
    },
    responseType: 'blob', // Expecting audio blob
  });
};

export default {
  sendVoiceQuery,
};
