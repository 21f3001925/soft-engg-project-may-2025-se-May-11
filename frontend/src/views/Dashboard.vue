<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import MedicationsSection from '../components/MedicationsSection.vue';
import AppointmentsSection from '../components/AppointmentsSection.vue';
import NewsFeedSection from '../components/NewsFeedSection.vue';
import EmergencyContactSection from '../components/EmergencyContactSection.vue';

const scheduleStore = useScheduleStore();

const currentTime = ref(new Date());
const greeting = ref('');

let timer = null;

const updateGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) greeting.value = 'Good Morning';
  else if (hour < 17) greeting.value = 'Good Afternoon';
  else greeting.value = 'Good Evening';
};

onMounted(async () => {
  await scheduleStore.fetchSchedules();
  timer = setInterval(() => {
    currentTime.value = new Date();
    updateGreeting();
  }, 1000);
  updateGreeting();
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<template>
  <div class="dashboard">
    <div
      class="flex items-center justify-between mb-8 p-6 rounded-2xl shadow bg-gradient-to-r from-blue-100 via-white to-purple-100 border border-blue-50 max-w-xl mx-auto"
    >
      <div>
        <h2
          class="dashboard-title text-2xl md:text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-1"
        >
          {{ greeting }}, Ramesh!
        </h2>
        <p class="text-xs text-gray-500 hidden md:block">Welcome to your health dashboard</p>
      </div>
      <div class="flex items-center space-x-2 bg-white/80 rounded-full px-4 py-2 shadow border border-gray-100">
        <span class="text-lg font-mono text-gray-700">{{
          currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }}</span>
      </div>
    </div>
    <EmergencyContactSection />
    <NewsFeedSection />
    <AppointmentsSection />
    <MedicationsSection />
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
}
</style>
