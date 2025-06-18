<script setup>
defineProps({
  schedule: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div class="schedule-item">
    <div class="schedule-time">{{ schedule.time }}</div>
    <div class="schedule-type" :class="schedule.type">
      {{ schedule.type }}
    </div>
    <div class="schedule-details">
      <h4>{{ schedule.name }}</h4>
      <p v-if="schedule.details">{{ schedule.details }}</p>
    </div>
  </div>
</template>

<style scoped>
.schedule-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.schedule-time {
  min-width: 80px;
  color: #666;
  font-weight: 500;
}

.schedule-type {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.schedule-type.appointment {
  background-color: #e3f2fd;
  color: #1976d2;
}

.schedule-type.medication {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.schedule-details {
  flex: 1;
}

.schedule-details h4 {
  margin: 0;
  color: #333;
}

.schedule-details p {
  margin: 0.25rem 0 0;
  color: #666;
  font-size: 0.9rem;
}
</style>
