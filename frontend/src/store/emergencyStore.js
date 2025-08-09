import { defineStore } from 'pinia';
//import mockApiService from '../services/mockApiService';
import emergencyService from '../services/emergencyService';

export const useEmergencyStore = defineStore('emergency', {
  state: () => ({
    contacts: [],
  }),

  actions: {
    async fetchContactsForSenior() {
      const response = await emergencyService.getEmergencyContacts();
      console.log('Fetched contacts:', response.data); // <-- Add this
      this.contacts = response.data.map(c => ({
        ...c,
        seniorId: c.seniorId ?? c.senior_id
      }));
    },

    async deleteContact(contactId) {
      await emergencyService.deleteEmergencyContact(contactId);
      this.contacts = this.contacts.filter((c) => c.contact_id !== contactId);
    },

    async addContact(contact) {
      const response = await emergencyService.addEmergencyContact(contact);
      this.contacts.push(response.data);
    },

    async updateContact(contact) {
      const { contact_id, name, relation, phone } = contact;
      const payload = { name, relation, phone }; // Only these 3 fields!
      const response = await emergencyService.updateEmergencyContact(contact_id, payload);
      const index = this.contacts.findIndex((c) => c.contact_id === contact_id);
      if (index !== -1) {
        this.contacts[index] = response.data;
      }
    },
  },
});
