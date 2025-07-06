import { defineStore } from 'pinia';
import mockApiService from '../services/mockApiService';

export const useNewsFeedStore = defineStore('newsFeed', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNewsFeed() {
      this.loading = true;
      this.error = null;
      try {
        const response = await mockApiService.getNewsfeed();
        this.news = response.data;
      } catch (e) {
        this.error = 'Failed to load news feed.';
      } finally {
        this.loading = false;
      }
    },
  },
});
