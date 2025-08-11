import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService.js';
import medicationService from '../services/medicationService';

export const useScheduleStore = defineStore('schedule', {
  state: () => ({
    schedule: {
      items: [],
      loading: false,
      error: null,
    },
    allMedications: {
      items: [],
      loading: false,
      error: null,
    },
  }),

  getters: {
    upcomingAppointments: (state) => {
      return state.schedule.items.filter((item) => item.type === 'appointment' || item.type === 'event');
    },
    medications: (state) => {
      return state.allMedications.items;
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

    async fetchAllMedications() {
      this.allMedications.loading = true;
      this.allMedications.error = null;
      try {
        const response = await medicationService.getMedications();
        this.allMedications.items = response.data;
      } catch (error) {
        this.allMedications.error = error;
      } finally {
        this.allMedications.loading = false;
      }
    },
  },
});
