<script setup>
import { onMounted, ref, computed } from 'vue';
import { useEventStore } from '../store/eventStore';

const eventStore = useEventStore();
const toastMessage = ref('');

onMounted(async () => {
  await eventStore.getEvents();
  await eventStore.fetchJoinedEventIds();
});

const events = computed(() => eventStore.events || []);
const joinedEventIds = computed(() => eventStore.joinedEventIds || []);

async function setReminder(event) {
  try {
    await eventStore.joinEvent(event.event_id);
    await eventStore.fetchJoinedEventIds(); // Refresh after joining
    showToast(`Reminder set and joined: "${event.name}"`);
  } catch (err) {
    showToast(eventStore.error || 'Failed to join event', 'error');
  }
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}
</script>

<template>
  <div class="events-page">
    <h1>Upcoming Events</h1>

    <div v-if="events.length === 0" class="empty">No upcoming events. Click below to add one!</div>

    <div v-else class="event-list">
      <div v-for="event in events" :key="event.event_id" class="event-card">
        <div class="event-info">
          <div class="event-title">{{ event.name }}</div>
          <div class="event-date">{{ event.date_time }}</div>
          <div class="event-location">{{ event.location }}</div>
        </div>
        <div class="event-actions">
          <button
            v-if="!joinedEventIds.includes(event.event_id)"
            class="reminder-button"
            @click="setReminder(event)"
          >
            Set Reminder
          </button>
          <span v-else style="color: green; font-weight: bold;">Reminder Set</span>
        </div>
      </div>
    </div>

    <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
  </div>
</template>

<style scoped>
.events-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
  color: #1480be;
  font-size: 2rem;
  text-align: center;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.event-list {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto;
  gap: 1rem;
}

.event-card {
  display: flex;
  justify-content: space-between;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  align-items: center;
  transition: box-shadow 0.2s ease;
}

.event-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.event-info {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1rem;
  width: 100%;
}

.event-title,
.event-date,
.event-location {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #111;
}

.event-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
}

.reminder-button {
  background-color: green;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.delete-button {
  background-color: red;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-button {
  margin-top: 20px;
  background-color: rgb(81, 188, 231);
  color: black;
  padding: 10px 16px;
  border: none;
  border-radius: 5px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;
}

.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #4caf50;
  color: white;
  padding: 12px 20px;
  border-radius: 5px;
  z-index: 9999;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  animation:
    fadein 0.3s ease,
    fadeout 0.3s ease 1.7s;
}

@keyframes fadein {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

@keyframes fadeout {
  from {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
}
</style>
