import axios from 'axios';

const API_URL = 'http://localhost:5001/api/v1/reminder';

const scheduleReminder = (reminderData) => {
  const token = localStorage.getItem('token');
  return axios.post(`${API_URL}/schedule-reminder`, reminderData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export default {
  scheduleReminder,
};
