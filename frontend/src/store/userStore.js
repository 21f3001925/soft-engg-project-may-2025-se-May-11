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
      profilePic: null,
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
    updateProfilePic(base64Image) {
      this.user.profilePic = base64Image;
    },
    setUser(userData) {
      this.user = { ...this.user, ...userData };
      if (userData.avatar_url) {
        this.user.profilePic = userData.avatar_url;
      }
    },
    setEmergencyContacts(contacts) {
      this.emergencyContacts = contacts;
    },
  },
});
