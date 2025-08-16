import axios from 'axios';

const API_URL = 'http://localhost:5001/api/reports';

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

const downloadReport = (reportId, format = 'pdf') => {
  const token = localStorage.getItem('token');
  let url = `${API_URL}/${reportId}/download`;
  let responseType = 'blob';

  if (format === 'text') {
    url += '?format=text';
    responseType = 'text';
  }

  return axios.get(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    responseType: responseType,
  });
};

export default {
  uploadReport,
  downloadReport,
};
