<script setup>
import { onMounted } from 'vue';
import { useSocialHubStore } from '../store/socialHubStore';
import { Heart, Users, ChevronRight, Sparkles } from 'lucide-vue-next';

const socialHubStore = useSocialHubStore();

onMounted(() => {
  socialHubStore.fetchSocialHubStats();
});
</script>

<template>
  <div
    class="mb-10 p-8 rounded-3xl shadow-xl border border-pink-100 bg-gradient-to-br from-white to-pink-50/30 flex flex-col justify-between min-h-[20rem]"
  >
    <div class="flex items-center text-2xl font-bold mb-2">
      <span
        class="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-r from-pink-500 to-rose-600 mr-4"
      >
        <Heart class="w-6 h-6 text-white" />
      </span>
      <span>Social Hub</span>
    </div>
    <div class="text-pink-600 text-sm mb-6 ml-14">
      {{
        socialHubStore.loading
          ? 'Loading...'
          : socialHubStore.stats
            ? socialHubStore.stats.subtitle
            : 'Connect & have fun!'
      }}
    </div>
    <div v-if="socialHubStore.error" class="text-red-500 text-center py-4">{{ socialHubStore.error }}</div>
    <div v-else class="text-center py-6">
      <div
        class="w-16 h-16 bg-gradient-to-r from-pink-100 to-rose-100 rounded-full flex items-center justify-center mx-auto mb-4"
      >
        <Users class="h-8 w-8 text-pink-600" />
      </div>
      <h4 class="font-semibold text-gray-900 mb-2">Discover Amazing Events</h4>
      <p class="text-sm text-gray-600 mb-4">Join local activities and meet wonderful people in your community</p>
      <div class="flex items-center justify-center space-x-4 text-xs text-gray-500 mb-4">
        <div class="flex items-center space-x-1">
          <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          <span>{{ socialHubStore.stats ? socialHubStore.stats.eventsToday : '-' }} events today</span>
        </div>
        <div class="flex items-center space-x-1">
          <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
          <span>{{ socialHubStore.stats ? socialHubStore.stats.eventsThisWeek : '-' }} this week</span>
        </div>
      </div>
      <router-link
        to="/events"
        class="w-full bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white transition-all duration-300 flex items-center justify-center gap-2 py-3 rounded-xl font-semibold shadow-sm hover:scale-105 active:scale-100 focus:outline-none focus:ring-2 focus:ring-pink-300"
      >
        <Sparkles class="w-5 h-5 mr-2" />
        Explore Events
        <ChevronRight class="w-5 h-5 ml-2" />
      </router-link>
    </div>
  </div>
</template>
