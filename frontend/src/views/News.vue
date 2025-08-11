<script setup>
import { ref } from 'vue';

const newsItems = ref([
  {
    id: 1,
    title: 'Elon Musk moves to Mars permanently',
    date: '2025-06-23',
    summary: 'Worlds richest guy, Elon makes Mars his new home.',
    link: '#',
  },
  {
    id: 2,
    title: 'Local Clinic Offers Free Checkups',
    date: '2025-06-22',
    summary: 'A neighborhood clinic is offering free health checkups for seniors this week.',
    link: '#',
  },
  {
    id: 3,
    title: '5 Tips for Medication Management',
    date: '2025-06-21',
    summary: 'Managing medications can be tricky. Here are 5 useful tips for staying on track.',
    link: '#',
  },
]);
</script>

<template>
  <div class="news-page">
    <h1>Daily Updates / News</h1>

    <div v-if="newsItems.length === 0" class="empty">No news updates available.</div>

    <div v-else class="news-list">
      <div v-for="item in newsItems" :key="item.id" class="news-card">
        <h2 class="news-title">{{ item.title }}</h2>
        <p class="news-date">{{ item.date }}</p>
        <p class="news-summary">{{ item.summary }}</p>
        <a class="news-link" :href="item.link">Read more</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.news-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
  color: #1480be;
  font-size: 2rem;
  text-align: center;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.news-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.news-date {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 1rem;
}

.news-summary {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: black;
}

.news-link {
  font-weight: bold;
  color: #00cec9;
  text-decoration: none;
}

.news-link:hover {
  text-decoration: underline;
}
</style>
