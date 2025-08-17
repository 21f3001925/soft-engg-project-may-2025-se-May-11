import axios from 'axios';

const API_URL = 'http://localhost:5000/api/chat';

const sendMessage = (reportId, message) => {
  const token = localStorage.getItem('token');
  return axios.post(
    `${API_URL}/${reportId}`,
    { message },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );
};

export default {
  sendMessage,
};
