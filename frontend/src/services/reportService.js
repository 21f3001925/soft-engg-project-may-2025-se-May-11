import axios from 'axios';

const API_URL = 'http://localhost:5000/api/reports';

const uploadReport = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const token = localStorage.getItem('token');

  return axios.post(`${API_URL}/summarize`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`,
    },
  });
};

const downloadReport = (reportId) => {
  const token = localStorage.getItem('token');
  return axios.get(`${API_URL}/${reportId}/download`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    responseType: 'blob', // Important for file downloads
  });
};

export default {
  uploadReport,
  downloadReport,
};
