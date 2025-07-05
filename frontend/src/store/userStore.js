import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      id: 1,
      username: 'Old Cat',
      age: 75,
      city: 'Noida',
      country: 'India',
      emergencyNumber: 1234567890,
      profilePic: null,
    },
    friends: {
      'Narendra Modi': 1234567890,
      'Elon Musk': 1234567890,
      'Donald Trump': 1234567890,
      'Vladimir Putin': 123456890,
    },
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
  },
});
