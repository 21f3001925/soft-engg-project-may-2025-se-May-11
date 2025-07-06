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
</script>

<template>
  <div class="schedule-item">
    <div class="schedule-time">{{ schedule.time }}</div>

    <div :class="['schedule-details', { compact: compactLayout }]">
      <!-- <h4>{{ schedule.name }}</h4> -->
      <h4 :class="customClass">{{ schedule.name }}</h4>

      <p v-if="schedule.details">{{ schedule.details }}</p>

      <div class="schedule-actions">
        <slot></slot>
      </div>
    </div>

    <div v-if="!hideType" class="schedule-type" :class="schedule.type">
      {{ schedule.type }}
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

.schedule-type.event {
  background-color: #bce8aa;
  color: #1b4d05;
}

.schedule-details {
  flex: 1;
}

.schedule-details.compact {
  display: flex; /* New layout only when compactLayout is true */
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.schedule-actions {
  display: flex; /* Make buttons side by side */
  gap: 0.5rem; /* Space between buttons */
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
