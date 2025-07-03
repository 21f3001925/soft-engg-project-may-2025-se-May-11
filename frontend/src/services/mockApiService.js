const mockSchedules = [
  { id: 1, type: 'medication', name: 'Meta', time: '08:00 AM', taken: true },
  { id: 2, type: 'medication', name: 'Gandalf', time: '08:00 AM', taken: false },
  {
    id: 3,
    type: 'appointment',
    name: 'Check-up with Mr.Raju',
    time: '11:30 AM',
    date: '06-07-2025',
    details: 'Room 201, Apollo J.Hills',
  },
  { id: 4, type: 'medication', name: 'Aspirin', time: '08:00 PM', taken: false },
  { id: 5, type: 'appointment', name: 'Game Night', time: '7:30 PM', date: '09-07-2025', details: 'Community Center' },
];

const newsFeed = [
  {
    id: 1,
    title: 'Old Bird Yells At Cloud',
    subtitle: 'Trending in Comedy',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    thumbnail:
      'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=facearea&w=64&h=64&facepad=2',
  },
  {
    id: 2,
    title: 'Elon Musk Moves To Mars Permanently',
    subtitle: 'Space News',
    time: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    thumbnail:
      'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=facearea&w=64&h=64&facepad=2',
  },
  {
    id: 3,
    title: 'New Health Guidelines Released',
    subtitle: 'Health',
    time: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    thumbnail:
      'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=facearea&w=64&h=64&facepad=2',
  },
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

  getNewsfeed() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: newsFeed });
      });
    });
  },
};
