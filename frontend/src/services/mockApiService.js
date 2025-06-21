const mockSchedules = [
  { id: 1, type: 'medication', name: 'Meta', time: '08:00 AM', taken: true },
  { id: 2, type: 'medication', name: 'Gandalf', time: '08:00 AM', taken: false },
  { id: 3, type: 'appointment', name: 'Check-up with Mr.Raju', time: '11:30 AM', details: 'Room 201' },
  { id: 4, type: 'medication', name: 'Aspirin', time: '08:00 PM', taken: false },
  { id: 5, type: 'appointment', name: 'Game Night', time: '7:30 PM', details: 'Community Center'},
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

  getAllMedications() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const allMedications = mockSchedules.filter((item) => item.type === 'medication');
        resolve({ data: allMedications });
      }, 500);
    });
  },
};
