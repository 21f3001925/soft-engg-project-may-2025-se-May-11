import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService';

export const useEmergencyStore = defineStore('emergency', {
  state: () => ({
    contacts: [],
  }),

  actions: {
    async fetchContactsForSenior(seniorId) {
      const response = await mockApiService.getEmergencyContacts(seniorId);
      this.contacts = response.data;
    },

    async deleteContact(contactId) {
      await mockApiService.deleteEmergencyContact(contactId);
      this.contacts = this.contacts.filter((c) => c.id !== contactId);
    },

    async addContact(contact) {
      const response = await mockApiService.addEmergencyContact(contact);
      this.contacts.push(response.data);
    },

    async updateContact(contact) {
      const response = await mockApiService.updateEmergencyContact(contact);
      const index = this.contacts.findIndex((c) => c.id === contact.id);
      if (index !== -1) {
        this.contacts[index] = response.data;
      }
    },
  },
});
