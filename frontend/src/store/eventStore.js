import { defineStore } from 'pinia';
import eventService from '../services/eventService';

export const useEventStore = defineStore('event', {
  state: () => ({
    events: [],
    loading: false,
    error: null,
  }),
  actions: {
    async getEvents() {
      this.loading = true;
      this.error = null;
      try {
        const response = await eventService.getEvents();
        this.events = response.data;
      } catch (err) {
        this.error = `Failed to load events: ${err.response?.data?.message || err.message}`;
      } finally {
        this.loading = false;
      }
    },

    async getAEvent(event_id) {
      this.loading = true;
      this.error = null;
      try {
        const response = await eventService.getAEvent(event_id);
        return response.data; // single event, not stored in array
      } catch (err) {
        this.error = `Failed to load event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async addEvent(eventData) {
      this.loading = true;
      this.error = null;
      try {
        await eventService.addEvents(eventData);
        await this.getEvents();
      } catch (err) {
        this.error = `Failed to add event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async updateEvent(event_id, eventData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await eventService.updateEvents(event_id, eventData);
        const index = this.events.findIndex((e) => e.id === event_id);
        if (index !== -1) {
          this.events[index] = response.data;
        }
      } catch (err) {
        this.error = `Failed to update event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async deleteEvent(event_id) {
      this.loading = true;
      this.error = null;
      try {
        await eventService.deleteEvents(event_id);
        await this.getEvents();
      } catch (err) {
        this.error = `Failed to delete event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async joinEvent(event_id) {
      this.loading = true;
      this.error = null;
      try {
        await eventService.joinAEvent(event_id);
        await this.getEvents();
      } catch (err) {
        this.error = `Failed to join event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
