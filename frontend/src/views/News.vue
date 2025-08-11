<script setup>
import { ref, onMounted, computed } from 'vue';
import { useNewsFeedStore } from '../store/newsFeedStore';
import { Search, Filter, Calendar } from 'lucide-vue-next';

const newsFeedStore = useNewsFeedStore();
const searchQuery = ref('');
const selectedCategory = ref('');
const isSearching = ref(false);

onMounted(async () => {
  await newsFeedStore.fetchCategories();
  if (!isSearching.value) {
    await newsFeedStore.fetchNewsFeed();
  }
});

const newsItems = computed(() => {
  return newsFeedStore.formattedNews;
});

const categories = computed(() => {
  return newsFeedStore.categories;
});

const handleSearch = async () => {
  if (searchQuery.value.trim() || selectedCategory.value) {
    isSearching.value = true;
    await newsFeedStore.searchNews(searchQuery.value.trim(), selectedCategory.value || null);
  } else {
    isSearching.value = false;
    await newsFeedStore.fetchNewsFeed();
  }
};

const clearSearch = async () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  isSearching.value = false;
  await newsFeedStore.fetchNewsFeed();
};

const formatDate = (dateString) => {
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateString;
  }
};
</script>

<template>
  <div class="p-8 max-w-6xl mx-auto bg-gray-50 min-h-screen">
    <div class="text-center mb-8">
      <h1 class="mb-2 text-blue-600 text-4xl font-bold">Daily Updates / News</h1>
      <p class="text-gray-600 text-lg mb-4">Stay informed with personalized news based on your interests</p>
    </div>

    <div class="bg-white p-6 rounded-2xl shadow-md border border-gray-100 mb-8">
      <div class="flex gap-4 items-center flex-wrap">
        <div class="relative flex-1 min-w-64">
          <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size="20" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search news..."
            class="w-full pl-12 pr-3 py-3 border-2 border-gray-200 rounded-xl text-base transition-colors focus:outline-none focus:border-blue-600"
            @keyup.enter="handleSearch"
          />
        </div>

        <div class="relative min-w-48">
          <Filter
            class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none z-10"
            size="20"
          />
          <select
            v-model="selectedCategory"
            class="w-full pl-12 pr-3 py-3 border-2 border-gray-200 rounded-xl text-base bg-white cursor-pointer transition-colors focus:outline-none focus:border-blue-600"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category.charAt(0).toUpperCase() + category.slice(1) }}
            </option>
          </select>
        </div>

        <button
          @click="handleSearch"
          class="px-6 py-3 border-none rounded-xl text-base font-semibold cursor-pointer transition-all bg-blue-600 text-white hover:bg-blue-700 hover:-translate-y-1"
        >
          Search
        </button>
        <button
          v-if="isSearching"
          @click="clearSearch"
          class="px-6 py-3 border-none rounded-xl text-base font-semibold cursor-pointer transition-all bg-gray-100 text-gray-700 hover:bg-gray-200"
        >
          Clear
        </button>
      </div>
    </div>

    <div v-if="newsFeedStore.loading" class="text-center py-12 text-gray-600">
      <div class="w-10 h-10 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
      <p>Loading news...</p>
    </div>

    <div
      v-else-if="newsFeedStore.error"
      class="text-center p-8 text-red-700 bg-red-50 border border-red-200 rounded-xl mb-8"
    >
      {{ newsFeedStore.error }}
    </div>

    <div v-else-if="newsItems.length === 0" class="text-center py-12 text-gray-600 bg-white rounded-2xl shadow-sm">
      <p>No news updates available.</p>
      <p v-if="isSearching" class="mt-4 text-sm">
        Try adjusting your search criteria or
        <button @click="clearSearch" class="bg-none border-none text-blue-600 underline cursor-pointer text-sm">
          view all news
        </button>
      </p>
    </div>

    <div v-else class="space-y-6">
      <div v-if="isSearching" class="mb-4 text-gray-600 text-sm">
        <p>{{ newsItems.length }} result{{ newsItems.length !== 1 ? 's' : '' }} found</p>
      </div>

      <div
        v-for="item in newsItems"
        :key="item.id"
        class="bg-white p-6 rounded-2xl shadow-sm transition-all duration-300 border border-gray-100 hover:-translate-y-1 hover:shadow-xl"
      >
        <div class="flex items-center gap-4 mb-4">
          <img
            :src="item.thumbnail"
            alt="News thumbnail"
            class="w-16 h-16 rounded-xl object-cover border-2 border-gray-100"
          />
          <div class="flex-1 flex flex-col gap-2">
            <span class="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-semibold w-fit">
              {{ item.category?.toUpperCase() || 'NEWS' }}
            </span>
            <div class="flex items-center gap-2 text-gray-600 text-sm">
              <Calendar size="14" />
              {{ formatDate(item.time) }}
            </div>
          </div>
        </div>

        <h2 class="text-xl font-bold mb-4 leading-snug">
          <a
            :href="item.url"
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-900 no-underline transition-colors hover:text-blue-600"
          >
            {{ item.title }}
          </a>
        </h2>

        <p v-if="item.description" class="text-base mb-6 text-gray-700 leading-relaxed">
          {{ item.description }}
        </p>

        <div class="flex justify-between items-center pt-4 border-t border-gray-100">
          <span class="text-gray-600 text-sm">{{ item.subtitle }}</span>
          <a
            :href="item.url"
            target="_blank"
            rel="noopener noreferrer"
            class="font-semibold text-blue-600 no-underline transition-all px-4 py-2 rounded-lg bg-blue-50 hover:bg-blue-100 hover:translate-x-1"
          >
            Read full article →
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
