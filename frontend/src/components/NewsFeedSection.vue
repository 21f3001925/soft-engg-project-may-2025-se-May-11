<script setup>
import { onMounted } from 'vue';
import { useNewsFeedStore } from '../store/newsFeedStore';
import { Coffee, ChevronRight, Zap } from 'lucide-vue-next';

const newsFeedStore = useNewsFeedStore();

onMounted(() => {
  newsFeedStore.fetchNewsFeed();
});

function timeAgo(isoTime) {
  const now = new Date();
  const then = new Date(isoTime);
  const diff = Math.floor((now - then) / 1000);
  if (diff < 60) return 'just now';
  if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
  if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
  return Math.floor(diff / 86400) + 'd ago';
}
</script>

<template>
  <div
    class="mb-10 p-8 rounded-3xl shadow-xl border border-green-100 bg-gradient-to-br from-white to-green-50/30 h-full"
  >
    <div class="flex items-center text-2xl font-bold mb-2">
      <span
        class="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-r from-green-500 to-emerald-600 mr-4"
      >
        <Zap class="w-6 h-6 text-white" />
      </span>
      <span>News Feed</span>
    </div>
    <div class="text-green-600 text-sm mb-6 ml-14">Latest updates and stories</div>
    <div class="space-y-4 ml-14">
      <div v-if="newsFeedStore.loading" class="text-gray-400 text-center py-4">Loading news...</div>
      <div v-else-if="newsFeedStore.error" class="text-red-500 text-center py-4">{{ newsFeedStore.error }}</div>
      <div
        v-else
        v-for="item in newsFeedStore.news"
        :key="item.id"
        class="group p-4 bg-white rounded-xl border border-gray-100 hover:border-green-200 hover:shadow-sm transition-all duration-300"
      >
        <div class="flex items-start space-x-3">
          <img :src="item.thumbnail" alt="thumbnail" class="w-8 h-8 rounded-full object-cover border border-gray-200" />
          <div>
            <p class="text-sm font-medium text-gray-900 group-hover:text-green-700 transition-colors">
              {{ item.title }}
            </p>
            <p class="text-xs text-gray-500 mt-1">{{ item.subtitle }} • {{ timeAgo(item.time) }}</p>
          </div>
        </div>
      </div>
    </div>
    <button
      class="mt-8 w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 hover:from-green-100 hover:to-emerald-100 transition-all duration-300 text-green-700 font-semibold shadow-sm hover:scale-105 active:scale-100 focus:outline-none focus:ring-2 focus:ring-green-300"
    >
      <Coffee class="w-5 h-5 mr-2" />
      Read More Stories
      <ChevronRight class="w-5 h-5 ml-2" />
    </button>
  </div>
</template>
