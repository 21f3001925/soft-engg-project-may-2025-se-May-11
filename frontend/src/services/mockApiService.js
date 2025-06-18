const mockSchedules = [
  { id: 1, type: 'medication', name: 'Meta', time: '08:00 AM', taken: true },
  { id: 2, type: 'medication', name: 'Gandalf', time: '08:00 AM', taken: false },
  { id: 3, type: 'appointment', name: 'Check-up with Mr.Raju', time: '11:30 AM', details: 'Room 201' },
  { id: 4, type: 'medication', name: 'Aspirin', time: '08:00 PM', taken: false },
];

export default {
  login() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            token: 'fake-jwt-token',
            user: { username: 'admin', role: 'admin' },
          },
          status: 200,
          statusText: 'OK',
        });
      }, 500);
    });
  },

  getSchedules() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: mockSchedules });
      }, 500);
    });
  },
};
