import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService';

export const useSocialHubStore = defineStore('socialHub', {
  state: () => ({
    stats: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchSocialHubStats() {
      this.loading = true;
      this.error = null;
      try {
        const response = await mockApiService.getSocialHubStats();
        this.stats = response.data;
      } catch (e) {
        this.error = 'Failed to load social hub stats.';
      } finally {
        this.loading = false;
      }
    },
  },
});
