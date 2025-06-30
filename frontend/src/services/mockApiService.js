const mockSchedules = [
  { id: 1, type: 'medication', name: 'Meta', time: '08:00 AM', taken: true },
  { id: 1, type: 'appointment', name: 'Hangout', time: '08:00 PM', details: 'Cafe' },
  { id: 2, type: 'medication', name: 'Gandalf', time: '08:00 AM', taken: false },
  { id: 3, type: 'appointment', name: 'Check-up with Mr.Raju', time: '11:30 AM', details: 'Room 201' },
  { id: 4, type: 'medication', name: 'Aspirin', time: '08:00 PM', taken: false },
  { id: 5, type: 'appointment', name: 'Game Night', time: '7:30 PM', details: 'Community Center' },
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
};
