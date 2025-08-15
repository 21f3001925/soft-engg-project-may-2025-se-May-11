import apiClient from './apiClient';

export default {
  async getSocialHubStats() {
    try {
      const eventsResponse = await apiClient.get('/events');
      const events = eventsResponse.data || [];

      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);
      const weekStart = new Date(today.getTime() - today.getDay() * 24 * 60 * 60 * 1000);
      const weekEnd = new Date(weekStart.getTime() + 7 * 24 * 60 * 60 * 1000);

      const eventsToday = events.filter((event) => {
        const eventDate = new Date(event.date_time);
        return eventDate >= today && eventDate < tomorrow;
      }).length;

      const eventsThisWeek = events.filter((event) => {
        const eventDate = new Date(event.date_time);
        return eventDate >= weekStart && eventDate < weekEnd;
      }).length;

      return {
        data: {
          eventsToday,
          eventsThisWeek,
          subtitle: 'Connect & have fun!',
          totalEvents: events.length,
        },
      };
    } catch (error) {
      console.error('Error fetching social hub stats:', error);
      throw error;
    }
  },
};
