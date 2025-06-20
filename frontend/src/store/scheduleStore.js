import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService.js';

export const useScheduleStore = defineStore('schedule', {
  state: () => ({
    schedule: {
      items: [],
      loading: false,
      error: null,
    },
    // you can more state objects here
  }),

  getters: {
    upcomingAppointments: (state) => {
      return state.schedule.items.filter((item) => item.type === 'appointment' && !item.taken);
    },
    medications: (state) => {
      return state.schedule.items.filter((item) => item.type === 'medication');
    },
  },

  actions: {
    async fetchSchedules() {
      this.schedule.loading = true;
      this.schedule.error = null;
      try {
        const response = await mockApiService.getSchedules();
        this.schedule.items = response.data;
      } catch (error) {
        this.schedule.error = error;
      } finally {
        this.schedule.loading = false;
      }
    },
  },
});
