import { defineStore } from 'pinia';
import caregiverService from '../services/caregiverService';

export const useCaregiverStore = defineStore('caregiver', {
  state: () => ({
    assignedSeniors: [],
    availableSeniors: [],
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
    async fetchAvailableSeniors() {
      try {
        const response = await caregiverService.getAvailableSeniors();
        this.availableSeniors = response.data;
      } catch (error) {
        console.error('Error fetching available seniors:', error);
      }
    },
    async assignCaregiverToSenior(senior_id) {
      await caregiverService.assignCaregiverToSenior(senior_id);
      await this.fetchAssignedSeniors();
      await this.fetchAvailableSeniors();
    },
    async removeCaregiverFromSenior(senior_id) {
      await caregiverService.removeCaregiverFromSenior(senior_id);
      await this.fetchAssignedSeniors();
      await this.fetchAvailableSeniors();
    },
  },
});
