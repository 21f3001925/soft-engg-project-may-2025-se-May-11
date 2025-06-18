<script setup>
import { onMounted } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import StatCard from '../components/StatCard.vue';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';

const scheduleStore = useScheduleStore();

onMounted(async () => {
  await scheduleStore.fetchSchedules();
});
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <div class="stats-section">
      <StatCard title="Upcoming Appointments" :value="scheduleStore.upcomingAppointments.length" />
      <StatCard title="Medications" :value="scheduleStore.medications.length" />
    </div>

    <div class="schedule-section">
      <h2>Today's Schedule</h2>
      <div v-if="scheduleStore.schedule.loading" class="loading">Loading schedules...</div>

      <div v-else-if="scheduleStore.schedule.error" class="error">
        {{ scheduleStore.schedule.error }}
      </div>

      <div v-else-if="scheduleStore.schedule.items.length === 0" class="empty">No schedules for today</div>

      <div v-else class="schedule-list">
        <ScheduleRowItem v-for="schedule in scheduleStore.schedule.items" :key="schedule.id" :schedule="schedule" />
      </div>
    </div>
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

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.schedule-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.schedule-section h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.schedule-list {
  display: flex;
  flex-direction: column;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}
</style>
