<script setup>
import { computed } from 'vue';

const props = defineProps({
  schedule: {
    type: Object,
    required: true,
  },
  isCaregiverView: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['mark-as-taken', 'edit', 'delete']);

const formattedTime = computed(() => {
  if (!props.schedule.time) return 'No time set';
  try {
    const date = new Date(props.schedule.time + 'Z');
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch (e) {
    console.error('Date formatting error:', e);
    return 'Invalid time';
  }
});
</script>

<template>
  <div class="schedule-item">
    <div class="schedule-info">
      <div class="schedule-time">{{ formattedTime }}</div>
      <div class="schedule-details">
        <p class="schedule-name">{{ schedule.name }}</p>
        <small class="schedule-dosage">Dosage: {{ schedule.dosage }}</small>
      </div>
    </div>

    <div class="schedule-actions">
      <template v-if="!isCaregiverView">
        <button
          v-if="!schedule.isTaken"
          class="action-button mark-as-taken-button"
          @click="emit('mark-as-taken', schedule)"
        >
          Mark as taken
        </button>
        <span v-else class="status-badge status-taken">Taken</span>
      </template>

      <template v-else>
        <span class="status-badge" :class="schedule.isTaken ? 'status-taken' : 'status-pending'">
          {{ schedule.isTaken ? 'Taken' : 'Pending' }}
        </span>
      </template>

      <button class="action-button edit-button" @click="emit('edit', schedule)">Edit</button>
      <button class="action-button delete-button" @click="emit('delete', schedule)">Delete</button>
    </div>
  </div>
</template>

<style scoped>
.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}
.schedule-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.schedule-time {
  font-weight: 700;
  font-size: 1.1rem;
  color: #1480be;
  width: 80px;
}
.schedule-name {
  font-weight: 500;
  margin: 0;
}
.schedule-dosage {
  color: #666;
}
.schedule-actions {
  display: flex;
  gap: 0.5rem;
}
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.8rem;
  color: #fff;
}
.status-taken {
  background-color: #28a745;
}
.status-pending {
  background-color: #ffc107;
  color: #333;
}
.action-button {
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 700;
  margin: 0 4px;
}
.edit-button {
  background-color: #3498db;
}
.mark-as-taken-button {
  background-color: #2ecc71;
}
.delete-button {
  background-color: #e74c3c;
}
</style>
