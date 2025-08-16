import apiClient from './apiClient';

class NewsService {
  async getCategories() {
    try {
      const response = await apiClient.get('/news/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching news categories:', error);
      throw error;
    }
  }

  /**
   * Get user's news categories from profile
   */
  async getUserNewsCategories() {
    try {
      const response = await apiClient.get('/profile');
      return response.data.news_categories || 'general'; // Default to general
    } catch (error) {
      console.error('Error fetching user news categories:', error);
      return 'general';
    }
  }

  /**
   * Get news articles based on query and category
   * @param {Object} params - Query parameters
   * @param {string} params.q - Search query (optional)
   * @param {string} params.category - News category (optional)
   */
  async getNews(params = {}) {
    try {
      const response = await apiClient.get('/news/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching news:', error);
      throw error;
    }
  }

  /**
   * Get news for user's selected categories
   * @param {string} userCategories - Comma-separated list of user's selected categories
   * @param {number} limit - Limit number of articles per category (optional)
   */
  async getNewsForUserCategories(userCategories, limit = 5) {
    if (!userCategories) {
      return this.getNews({ category: 'general' });
    }

    try {
      const categories = userCategories.split(',').map((cat) => cat.trim());
      const newsPromises = categories.map((category) =>
        this.getNews({ category }).catch((error) => {
          console.error(`Error fetching news for category ${category}:`, error);
          return { articles: [] };
        }),
      );

      const results = await Promise.all(newsPromises);

      let allArticles = [];
      results.forEach((result, index) => {
        if (result.articles && result.articles.length > 0) {
          const categoryArticles = result.articles.slice(0, limit).map((article) => ({
            ...article,
            category: categories[index],
            id: `${categories[index]}-${article.url || Date.now()}-${Math.random()}`,
          }));
          allArticles = allArticles.concat(categoryArticles);
        }
      });

      allArticles.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

      return {
        status: 'ok',
        totalResults: allArticles.length,
        articles: allArticles.slice(0, 20),
      };
    } catch (error) {
      console.error('Error fetching news for user categories:', error);
      throw error;
    }
  }
}

export default new NewsService();
