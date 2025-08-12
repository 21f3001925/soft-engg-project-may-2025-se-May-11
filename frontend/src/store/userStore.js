import { defineStore } from 'pinia';
import accessibilityService from '../services/accessibilityService';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      id: 1,
      username: 'Old Cat',
      age: 75,
      city: 'Noida',
      country: 'India',
      phone_number: 1234567890,
    },
    emergencyContacts: [],
    stats: {
      topicsLiked: 200,
      commentsPosted: 50,
      appointmentsMissed: 2,
      medicationsMissed: 6,
      totalScreentime: 200,
    },
    accessibility: {
      fontSize: 'small',
      darkMode: false,
    },
  }),

  actions: {
    setEmergencyContacts(contacts) {
      this.emergencyContacts = contacts;
    },
    async setUser(userData) {
      this.user = { ...this.user, ...userData };
      if (userData.avatar_url) {
        this.user.profilePic = userData.avatar_url;
      }
      await this.fetchAccessibilitySettings();
    },
    async fetchAccessibilitySettings() {
      try {
        const settings = await accessibilityService.getAccessibilitySettings();
        this.accessibility.fontSize = settings.font_size || 'small';
        this.accessibility.darkMode = settings.theme === 'dark';
      } catch (error) {
        console.error('Failed to fetch accessibility settings:', error);
      }
    },
    async initialize() {
      const token = localStorage.getItem('token');
      if (token) {
        await this.fetchAccessibilitySettings();
      }
    },
    async updateFontSize(newSize) {
      console.log('userStore.js: updateFontSize action called with', newSize);
      this.accessibility.fontSize = newSize;
      try {
        await accessibilityService.updateAccessibilitySettings({ font_size: newSize });
      } catch (error) {
        console.error('Failed to update font size:', error);
      }
    },
    async updateDarkMode(newMode) {
      console.log('userStore.js: updateDarkMode action called with', newMode);
      this.accessibility.darkMode = newMode;
      try {
        await accessibilityService.updateAccessibilitySettings({ theme: newMode ? 'dark' : 'light' });
      } catch (error) {
        console.error('Failed to update dark mode:', error);
      }
    },
  },
});
