import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
  }),
  actions: {
    fetchNotifications() {
      // Placeholder for fetching notifications
      console.log('Fetching notifications (placeholder)');
    },
    markAllAsRead() {
      // Placeholder for marking all as read
      console.log('Marking all notifications as read (placeholder)');
      this.notifications = [];
    },
    dismissNotification(id) {
      // Placeholder for dismissing a specific notification
      console.log(`Dismissing notification ${id} (placeholder)`);
      this.notifications = this.notifications.filter((n) => n.id !== id);
    },
  },
});
