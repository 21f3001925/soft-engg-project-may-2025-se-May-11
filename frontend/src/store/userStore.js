import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      username: 'Old Cat',
      age: 75,
      city: 'Noida',
      country: 'India',
      emergencyNumber: 1234567890,
    },
    friends: ['Narendra Modi', 'Elon Musk', 'Donald Trump', 'Vladimir Putin'],
    stats: {
      topicsLiked: 200,
      commentsPosted: 50,
      appointmentsMissed: 2,
      medicationsMissed: 6,
      totalScreentime: 200,
    },
  }),
});
