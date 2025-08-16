import { defineStore } from 'pinia';
import socialService from '../services/socialService';

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
        const response = await socialService.getSocialHubStats();
        this.stats = response.data;
      } catch (e) {
        console.error('Error fetching social hub stats:', e);
        this.error = 'Failed to load social hub stats.';
      } finally {
        this.loading = false;
      }
    },
  },
});
