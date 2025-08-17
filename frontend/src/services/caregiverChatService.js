import axios from 'axios';

const API_URL = 'http://localhost:5001/api/caregiver-chat';

const sendMessage = (seniorId, message) => {
  const token = localStorage.getItem('token');
  return axios.post(
    `${API_URL}/${seniorId}`,
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
