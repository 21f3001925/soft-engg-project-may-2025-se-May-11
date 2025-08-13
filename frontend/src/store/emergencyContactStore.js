import { defineStore } from 'pinia';
import emergencyService from '../services/emergencyService';

export const useEmergencyContactStore = defineStore('emergencyContact', {
  state: () => ({
    contacts: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchEmergencyContact() {
      this.loading = true;
      this.error = null;
      try {
        const response = await emergencyService.getEmergencyContacts();
        this.contacts = response.data;
      } catch (e) {
        this.error = 'Failed to load emergency contact.';
      } finally {
        this.loading = false;
      }
    },
  },
});
