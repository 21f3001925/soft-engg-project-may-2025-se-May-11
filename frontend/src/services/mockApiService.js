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
  { id: 4, type: 'medication', name: 'Aspirin', time: '08:00 PM', isTaken: false },
  { id: 5, type: 'appointment', name: 'Game Night', time: '7:30 PM', date: '09-07-2025', details: 'Community Center' },
  { id: 6, type: 'event', name: 'Game Night', time: '7:30 PM', details: 'Community Center' },
  { id: 7, type: 'event', name: 'Hangout', time: '08:00 PM', details: 'Cafe' },
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

const emergencyContact = {
  name: 'Ramesh A',
  phone: '(918) 123-4567',
  subtitle: '24/7 support',
};

const socialHubStats = {
  eventsToday: 3,
  eventsThisWeek: 12,
  subtitle: 'Connect & have fun!',
};

const notifications = [
  { id: 1, text: 'Appointment at 11:30 AM' },
  { id: 2, text: 'New message from Social Hub' },
];

let mockEmergencyContacts = [
  { id: 1, seniorId: 1, name: 'Daughter', phone: '9876543210' },
  { id: 2, seniorId: 1, name: 'Son', phone: '8765432109' },
  { id: 3, seniorId: 2, name: 'Neighbor', phone: '9988776655' },
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

  getEmergencyContact() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: emergencyContact });
      }, 300);
    });
  },

  getSocialHubStats() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: socialHubStats });
      }, 300);
    });
  },

  getNotifications() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: notifications });
      }, 300);
    });
  },

  getEmergencyContacts(seniorId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const contacts = mockEmergencyContacts.filter((c) => c.seniorId === seniorId);
        resolve({ data: contacts });
      }, 500);
    });
  },

  deleteEmergencyContact(contactId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        mockEmergencyContacts = mockEmergencyContacts.filter((c) => c.id !== contactId);
        resolve({ status: 200 });
      }, 500);
    });
  },

  addEmergencyContact(contact) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newContact = { ...contact, id: Date.now() };
        mockEmergencyContacts.push(newContact);
        resolve({ data: newContact });
      }, 500);
    });
  },

  updateEmergencyContact(contact) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const index = mockEmergencyContacts.findIndex((c) => c.id === contact.id);
        if (index !== -1) {
          mockEmergencyContacts[index] = { ...contact };
        }
        resolve({ data: contact });
      }, 500);
    });
  },

  addAppointment(event) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newEvent = { ...event, id: Date.now(), type: 'appointment' };
        mockSchedules.push(newEvent);
        resolve({ data: newEvent });
      }, 500);
    });
  },

  updateAppointment(event) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const index = mockSchedules.findIndex((e) => e.id === event.id);
        if (index !== -1) {
          mockSchedules[index] = { ...event };
        }
        resolve({ data: event });
      }, 500);
    });
  },

  deleteAppointment(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const index = mockSchedules.findIndex((e) => e.id === id);
        if (index !== -1) mockSchedules.splice(index, 1);
        resolve({ status: 200 });
      }, 500);
    });
  },
};
