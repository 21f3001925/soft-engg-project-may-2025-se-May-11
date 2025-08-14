<script setup>
defineProps({
  schedule: {
    type: Object,
    required: true,
  },
});

const formattedTime = (dateStr) => {
  if (!dateStr) return 'No time specified';
  return new Date(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>

<template>
  <div class="schedule-item">
    <div class="item-details">
      <div class="item-title">{{ schedule.name || schedule.title }}</div>
      <div class="item-time">Time: {{ formattedTime(schedule.date_time || schedule.time) }}</div>
      <div v-if="schedule.location" class="item-location">Location: {{ schedule.location }}</div>
      <div v-if="schedule.dosage" class="item-dosage">Dosage: {{ schedule.dosage }}</div>
    </div>
    <div class="item-actions">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
}
.item-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.item-title {
  font-weight: 600;
  color: #333;
}
.item-time,
.item-location,
.item-dosage {
  font-size: 0.9rem;
  color: #666;
}
.item-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
