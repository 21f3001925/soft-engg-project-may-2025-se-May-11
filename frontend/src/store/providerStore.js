import { defineStore } from 'pinia';
import providerService from '../services/providerService';

export const useProviderStore = defineStore('provider', {
  state: () => ({
    providers: [],
    loading: false,
    error: null,
    events: [],
    attendees: {},
  }),
  actions: {
    async fetchEvents() {
      this.loading = true;
      this.error = null;
      try {
        const response = await providerService.getEvents();
        this.events = response.data;
      } catch (err) {
        this.error = `Failed to load events: ${err.response?.data?.message || err.message}`;
      } finally {
        this.loading = false;
      }
    },
    async addEvent(eventData) {
      this.loading = true;
      this.error = null;
      try {
        await providerService.addEvent(eventData);
        await this.fetchEvents();
      } catch (err) {
        this.error = `Failed to add event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateEvent(id, eventData) {
      this.loading = true;
      this.error = null;
      try {
        await providerService.updateEvent(id, eventData); // id in URL, eventData as body
        await this.fetchEvents();
      } catch (err) {
        this.error = `Failed to update event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async deleteEvent(id) {
      this.loading = true;
      this.error = null;
      try {
        await providerService.deleteEvent(id);
        await this.fetchEvents();
      } catch (err) {
        this.error = `Failed to delete event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchEventAttendees(event_id) {
      this.loading = true;
      this.error = null;
      try {
        const response = await providerService.getEventAttendees(event_id);
        this.attendees[event_id] = response.data;
        return response.data;
      } catch (err) {
        this.error = `Failed to fetch attendees: ${err.response?.data?.message || err.message}`;
        return [];
      } finally {
        this.loading = false;
      }
    },
    async removeAttendee(event_id, senior_id) {
      this.loading = true;
      this.error = null;
      try {
        await providerService.removeAttendee(event_id, senior_id);
        await this.fetchEventAttendees(event_id);
      } catch (err) {
        this.error = `Failed to remove attendee: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
