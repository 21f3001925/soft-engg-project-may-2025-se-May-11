import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      id: 1,
      username: 'Old Cat',
      age: 75,
      city: 'Noida',
      country: 'India',
      phone_number: 1234567890,
    },
    emergencyContacts: [],
    stats: {
      topicsLiked: 200,
      commentsPosted: 50,
      appointmentsMissed: 2,
      medicationsMissed: 6,
      totalScreentime: 200,
    },
    accessibility: {
      fontSize: 'small',
      darkMode: false,
    },
  }),

  actions: {
    setUser(userData) {
      this.user = { ...this.user, ...userData };
    },
    setEmergencyContacts(contacts) {
      this.emergencyContacts = contacts;
    },
  },
});
