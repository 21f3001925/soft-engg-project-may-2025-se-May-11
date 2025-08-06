import { defineStore } from 'pinia';
import medicationService from '../services/medicationService';

export const useMedicationStore = defineStore('medication', {
  state: () => ({
    medications: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMedications() {
      this.loading = true;
      this.error = null;
      try {
        const response = await medicationService.getMedications();
        this.medications = response.data;
      } catch (err) {
        this.error = `Failed to load medications: ${err.response?.data?.message || err.message}`;
      } finally {
        this.loading = false;
      }
    },
    async addMedication(medicationData) {
      this.loading = true;
      this.error = null;
      try {
        await medicationService.addMedication(medicationData);
        await this.fetchMedications();
      } catch (err) {
        this.error = `Failed to add medication: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateMedication(id, medicationData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await medicationService.updateMedication(id, medicationData);
        const index = this.medications.findIndex((m) => m.medication_id === id);
        if (index !== -1) {
          this.medications[index] = response.data;
        }
      } catch (err) {
        this.error = `Failed to update medication: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async deleteMedication(id) {
      this.loading = true;
      this.error = null;
      try {
        await medicationService.deleteMedication(id);
        this.medications = this.medications.filter((m) => m.medication_id !== id);
      } catch (err) {
        this.error = `Failed to delete medication: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
