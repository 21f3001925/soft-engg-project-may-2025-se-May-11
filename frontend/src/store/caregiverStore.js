import { defineStore } from 'pinia';

export const useCaregiverStore = defineStore('caregiver', {
  state: () => ({
    assignedSeniors: [
      {
        id: 1,
        name: 'Old Cat',
        age: 75,
        city: 'Noida',
        phone: '1234567890',
        medications: [
          { id: 1, name: 'Paracetamol', taken: false },
          { id: 2, name: 'Ibuprofen', taken: false },
        ],
        appointments: [{ id: 1, date: '2025-06-21', purpose: 'Routine checkup' }],
      },
      {
        id: 2,
        name: 'Old Dog',
        age: 80,
        city: 'Vadodara',
        phone: '0987654321',
        medications: [{ id: 3, name: 'Aspirin', taken: true }],
        appointments: [{ id: 2, date: '2025-06-22', purpose: 'Dental checkup' }],
      },
    ],
  }),

  actions: {
    markMedicationAsTaken(seniorId, medId) {
      const senior = this.assignedSeniors.find((s) => s.id === seniorId);
      if (senior) {
        const med = senior.medications.find((m) => m.id === medId);
        if (med) med.isTaken = true;
      }
    },

    deleteAppointment(seniorId, apptId) {
      const senior = this.assignedSeniors.find((s) => s.id === seniorId);
      if (senior) {
        senior.appointments = senior.appointments.filter((a) => a.id !== apptId);
      }
    },

    async fetchAssignedSeniors() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(this.assignedSeniors);
        }, 500);
      });
    },
  },
});
