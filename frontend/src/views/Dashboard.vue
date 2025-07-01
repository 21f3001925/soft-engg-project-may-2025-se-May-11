<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import StatCard from '../components/StatCard.vue';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import MedicationsSection from '../components/MedicationsSection.vue';

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

function toggleMedication(id) {
  scheduleStore.medications = scheduleStore.medications.map((med) =>
    med.id === id ? { ...med, taken: !med.taken } : med,
  );
}
</script>

<template>
  <div class="dashboard">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem">
      <div>
        <h2>{{ greeting }}, Ramesh!</h2>
      </div>
      <div style="font-family: monospace; color: #555">
        {{ currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
      </div>
    </div>
    <MedicationsSection />
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
}
</style>
