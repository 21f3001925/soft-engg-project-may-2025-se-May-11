import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService';

export const useEmergencyContactStore = defineStore('emergencyContact', {
  state: () => ({
    contact: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchEmergencyContact() {
      this.loading = true;
      this.error = null;
      try {
        const response = await mockApiService.getEmergencyContact();
        this.contact = response.data;
      } catch (e) {
        this.error = 'Failed to load emergency contact.';
      } finally {
        this.loading = false;
      }
    },
  },
});
