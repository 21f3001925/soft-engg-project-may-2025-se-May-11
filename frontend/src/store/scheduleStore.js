import { defineStore } from 'pinia';
import appointmentService from '../services/appointmentService.js';
import medicationService from '../services/medicationService.js';

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
    async getAppointments() {
      this.schedule.loading = true;
      this.schedule.error = null;
      try {
        const response = await appointmentService.getAppointments();

        if (Array.isArray(response.data)) {
          this.schedule.items = response.data.map((appt) => ({
            id: appt.appointment_id,
            title: appt.title,
            date_time: appt.date_time,
            location: appt.location,
            reminder_time: appt.reminder_time || null,
            type: appt.type || 'appointment', // so filtering works
          }));
        } else {
          this.schedule.items = [];
        }
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

        this.allMedications.items = response.data.map((med) => ({
          id: med.medication_id,
          name: med.name,
          dosage: med.dosage,
          time: med.time,
          taken: med.isTaken,
          senior_id: med.senior_id,
        }));
      } catch (error) {
        this.allMedications.error = error;
      } finally {
        this.allMedications.loading = false;
      }
    },

    async toggleMedication(medicationId) {
      try {
        const medication = this.allMedications.items.find((med) => med.id === medicationId);
        if (!medication) return;

        const newTakenStatus = !medication.taken;

        medication.taken = newTakenStatus;

        await medicationService.updateMedication(medicationId, {
          isTaken: newTakenStatus,
        });

        await this.fetchAllMedications();
      } catch (error) {
        console.error('Error toggling medication:', error);
        const medication = this.allMedications.items.find((med) => med.id === medicationId);
        if (medication) {
          medication.taken = !medication.taken;
        }
      }
    },
  },
});
