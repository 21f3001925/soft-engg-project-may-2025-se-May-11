import { defineStore } from 'pinia';
import caregiverService from '../services/caregiverService';

export const useCaregiverStore = defineStore('caregiver', {
  state: () => ({
    assignedSeniors: [],
  }),

  actions: {
    async fetchAssignedSeniors() {
      try {
        const response = await caregiverService.getAssignedSeniors();
        this.assignedSeniors = response.data;
      } catch (error) {
        console.error('Error fetching assigned seniors:', error);
      }
    },
  },
});
