import { defineStore } from 'pinia';
import accessibilityService from '../services/accessibilityService';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    selectedSeniorId: null,
    accessibility: {
      fontSize: 'medium',
      darkMode: false,
    },
  }),

  getters: {
    displayName: (state) => state.user?.username || 'Guest User',
  },

  actions: {
    async setUser(userData) {
      try {
        this.user = { ...this.user, ...userData };
        await this.fetchAccessibilitySettings();
      } catch (error) {
        console.error('Error setting user data:', error);
      }
    },

    setSelectedSeniorId(seniorId) {
      this.selectedSeniorId = seniorId;
    },

    logout() {
      this.user = null;
      this.selectedSeniorId = null;
      this.accessibility = {
        fontSize: 'medium',
        darkMode: false,
      };
      localStorage.removeItem('token');
    },
    async fetchAccessibilitySettings() {
      try {
        const settings = await accessibilityService.getAccessibilitySettings();
        this.accessibility.fontSize = settings.font_size || 'medium';
        this.accessibility.darkMode = settings.theme === 'dark';
      } catch (error) {
        console.error('Failed to fetch accessibility settings:', error);
      }
    },

    async initialize() {
      try {
        const token = localStorage.getItem('token');
        if (token && !this.user) {
          await this.fetchAccessibilitySettings();
        }
      } catch (error) {
        console.error('Initialization error:', error);
      }
    },
    async updateFontSize(newSize) {
      this.accessibility.fontSize = newSize;
      try {
        await accessibilityService.updateAccessibilitySettings({ font_size: newSize });
      } catch (error) {
        console.error('Failed to update font size:', error);
      }
    },
    async updateDarkMode(newMode) {
      this.accessibility.darkMode = newMode;
      try {
        await accessibilityService.updateAccessibilitySettings({ theme: newMode ? 'dark' : 'light' });
      } catch (error) {
        console.error('Failed to update dark mode:', error);
      }
    },
  },
});
