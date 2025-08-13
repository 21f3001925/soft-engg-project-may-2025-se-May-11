<script setup>
defineProps({
  schedule: {
    type: Object,
    required: true,
  },
  customClass: {
    type: String,
    default: '',
  },
  hideType: {
    type: Boolean,
    default: false,
  },
  compactLayout: {
    type: Boolean,
    default: false,
  },
});

function formatTime(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  const options = {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };
  return date.toLocaleTimeString('en-US', options);
}
</script>

<template>
  <div class="schedule-row">
    <div class="event-name">{{ schedule.name }}</div>
    <div class="event-description">{{ schedule.description }}</div>
    <div class="event-location">{{ schedule.location }}</div>
    <div class="event-time">{{ formatTime(schedule.date_time) }}</div>
    <slot></slot>
  </div>
</template>

<style scoped>
.schedule-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}
.event-name {
  flex: 1;
  color: #333;
  font-weight: 500;
}
.event-description {
  flex: 2;
  color: #666;
  font-size: 0.9rem;
}
.event-time {
  min-width: 80px;
  color: #666;
  font-weight: 500;
}
</style>
