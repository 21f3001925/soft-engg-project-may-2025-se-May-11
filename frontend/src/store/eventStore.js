import { defineStore } from 'pinia';
import eventService from '../services/eventService';

export const useEventStore = defineStore('event', {
  state: () => ({
    events: [],
    loading: false,
    error: null,
    joinedEventIds: [],
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

    async fetchJoinedEventIds() {
      this.loading = true;
      this.error = null;
      try {
        // You need a backend endpoint like: GET /api/v1/events/joined
        const response = await eventService.getJoinedEvents();
        // Assume response.data is an array of event_ids
        this.joinedEventIds = response.data.event_ids;
      } catch (err) {
        this.error = `Failed to fetch joined events: ${err.response?.data?.message || err.message}`;
      } finally {
        this.loading = false;
      }
    },

    async unjoinEvent(event_id) {
      this.loading = true;
      this.error = null;
      try {
        await eventService.unjoinEvent(event_id);
        await this.fetchJoinedEventIds();
      } catch (err) {
        this.error = `Failed to cancel event: ${err.response?.data?.message || err.message}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
