import { defineStore } from 'pinia';
import newsService from '../services/newsService';

export const useNewsFeedStore = defineStore('newsFeed', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
    categories: [],
  }),

  getters: {
    formattedNews: (state) => {
      return state.news.map((article) => ({
        id: article.id || `${article.url}-${Date.now()}`,
        title: article.title,
        subtitle: `${article.source?.name || 'News'} • ${article.category || 'General'}`,
        time: article.publishedAt,
        thumbnail:
          article.urlToImage ||
          'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=facearea&w=64&h=64&facepad=2',
        url: article.url,
        description: article.description,
        category: article.category,
      }));
    },
  },

  actions: {
    async fetchCategories() {
      try {
        const response = await newsService.getCategories();
        this.categories = response.categories || [];
      } catch (error) {
        console.error('Failed to fetch news categories:', error);
      }
    },

    async fetchNewsFeed() {
      this.loading = true;
      this.error = null;
      try {
        const userCategories = await newsService.getUserNewsCategories();
        const response = await newsService.getNewsForUserCategories(userCategories);
        this.news = response.articles || [];
      } catch (error) {
        this.error = 'Failed to load news feed.';
        try {
          const fallbackResponse = await newsService.getNews({ category: 'general' });
          this.news = (fallbackResponse.articles || []).slice(0, 10);
        } catch (fallbackError) {
          this.news = [];
        }
      } finally {
        this.loading = false;
      }
    },

    async searchNews(query, category = null) {
      this.loading = true;
      this.error = null;
      try {
        const response = await newsService.getNews({ q: query, category });
        this.news = response.articles || [];
      } catch (error) {
        console.error('Failed to search news:', error);
        this.error = 'Failed to search news.';
        this.news = [];
      } finally {
        this.loading = false;
      }
    },
  },
});
