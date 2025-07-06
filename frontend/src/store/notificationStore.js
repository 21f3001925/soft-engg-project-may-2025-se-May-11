import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNotifications() {
      this.loading = true;
      this.error = null;
      try {
        const response = await mockApiService.getNotifications();
        this.notifications = response.data;
      } catch (e) {
        this.error = 'Failed to load notifications.';
      } finally {
        this.loading = false;
      }
    },
    markAllAsRead() {
      this.notifications = [];
    },
    dismissNotification(id) {
      this.notifications = this.notifications.filter((n) => n.id !== id);
    },
  },
});
