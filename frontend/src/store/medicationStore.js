import { defineStore } from 'pinia';
import medicationService from '../services/medicationService';

export const useMedicationStore = defineStore('medication', {
  state: () => ({
    medications: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMedications(seniorId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await medicationService.getMedications(seniorId);
        this.medications = response.data;
      } catch (err) {
        this.error = `Failed to load medications: ${err.response?.data?.message || err.message}`;
      } finally {
        this.loading = false;
      }
    },
    async addMedication(medicationData, seniorId) {
      this.loading = true;
      this.error = null;
      try {
        await medicationService.addMedication(medicationData, seniorId);
        await this.fetchMedications(seniorId);
      } catch (err) {
        this.error = `Failed to add medication: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateMedication(id, medicationData, seniorId) {
      this.loading = true;
      this.error = null;
      try {
        const payload = {
          name: medicationData.name,
          dosage: medicationData.dosage,
          time: medicationData.time,
          isTaken: medicationData.isTaken,
        };

        Object.keys(payload).forEach((key) => {
          if (payload[key] === undefined) {
            delete payload[key];
          }
        });

        const response = await medicationService.updateMedication(id, payload, seniorId);
        const index = this.medications.findIndex((m) => m.medication_id === id);
        if (index !== -1) {
          this.medications[index] = { ...this.medications[index], ...response.data };
        }
      } catch (err) {
        this.error = `Failed to update medication: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async deleteMedication(id, seniorId) {
      this.loading = true;
      this.error = null;
      try {
        await medicationService.deleteMedication(id, seniorId);
        this.medications = this.medications.filter((m) => m.medication_id !== id);
      } catch (err) {
        this.error = `Failed to delete medication: ${err.response?.data?.message || err.message}`;
        await this.fetchMedications(seniorId);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // --- FIX: Restored the missing markAsTaken function ---
    async markAsTaken(medication) {
      try {
        // The seniorId will be undefined for the senior's own view, which is correct.
        await this.updateMedication(medication.medication_id, { isTaken: true }, medication.senior_id);
      } catch (err) {
        // Error will be caught and displayed by the updateMedication action
        console.error('Failed to mark as taken:', err);
      }
    },
  },
});
