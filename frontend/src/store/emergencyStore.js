import { defineStore } from 'pinia';
import emergencyService from '../services/emergencyService';

export const useEmergencyStore = defineStore('emergency', {
  state: () => ({
    contacts: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchContactsForSenior(seniorId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await emergencyService.getEmergencyContacts(seniorId);
        this.contacts = response.data;
      } catch (error) {
        this.error = 'Failed to load emergency contacts.';
      } finally {
        this.loading = false;
      }
    },

    async deleteContact(contactId, seniorId) {
      await emergencyService.deleteEmergencyContact(contactId, seniorId);
      this.contacts = this.contacts.filter((c) => c.contact_id !== contactId);
    },

    async addContact(contactPayload, seniorId) {
      const response = await emergencyService.addEmergencyContact(contactPayload, seniorId);
      const newContact = {
        ...response.data,
        seniorId: response.data.seniorId ?? response.data.senior_id,
      };
      this.contacts.push(newContact);
    },

    async updateContact(contact) {
      const { contact_id, name, relation, phone, senior_id } = contact;
      const payload = { name, relation, phone };
      // The senior_id can be undefined here for a senior, which is fine.
      const response = await emergencyService.updateEmergencyContact(contact_id, payload, senior_id);
      const index = this.contacts.findIndex((c) => c.contact_id === contact_id);
      if (index !== -1) {
        this.contacts[index] = response.data;
      }
    },
  },
});
