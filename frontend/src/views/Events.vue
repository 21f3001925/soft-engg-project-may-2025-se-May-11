<script setup>
import { onMounted, computed, ref } from 'vue';
import { useUserStore } from '../store/userStore';
import { useEventStore } from '../store/eventStore';

const userStore = useUserStore();
const eventStore = useEventStore();

const toastMessage = ref('');
const toastType = ref('success');

onMounted(async () => {
  await eventStore.getEvents();
  await eventStore.fetchJoinedEventIds();
});

const events = computed(() => eventStore.events || []);
const joinedEventIds = computed(() => eventStore.joinedEventIds || []);

// This function converts the UTC time from the server back to local time
function formatDisplayDateTime(isoString) {
  if (!isoString) return 'No date provided';
  const date = new Date(isoString);
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  };
  return date.toLocaleString(undefined, options);
}

async function handleJoinEvent(event) {
  try {
    await eventStore.joinEvent(event.event_id);
    showToast(`Successfully joined event: "${event.name}"`);
  } catch (err) {
    showToast(eventStore.error || 'Failed to join event', 'error');
  }
}

async function cancelReminder(event) {
  try {
    await eventStore.unjoinEvent(event.event_id);
    showToast(`You have left the event: "${event.name}"`);
  } catch (err) {
    showToast(eventStore.error || 'Failed to cancel reminder', 'error');
  }
}

function showToast(message, type = 'success') {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = '';
  }, 3000);
}
</script>

<template>
  <div class="events-page">
    <h1>Upcoming Events</h1>

    <div v-if="events.length === 0" class="empty">No upcoming events.</div>

    <div v-else class="event-list">
      <div v-for="event in events" :key="event.event_id" class="event-card">
        <div class="event-info">
          <div class="event-title">{{ event.name }}</div>
          <div class="event-date">{{ formatDisplayDateTime(event.date_time) }}</div>
          <div class="event-description">{{ event.description }}</div>
          <div class="event-location">{{ event.location }}</div>
        </div>
        <div class="event-actions">
          <button
            v-if="!joinedEventIds.includes(event.event_id)"
            class="reminder-button"
            @click="handleJoinEvent(event)"
          >
            Join Event & Set Reminder
          </button>
          <span v-else>
            <span style="color: green; font-weight: bold">✓ Joined</span>
            <button class="cancel-button" @click="cancelReminder(event)" style="margin-left: 10px">Cancel</button>
          </span>
        </div>
      </div>
    </div>

    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>
  </div>
</template>

<style scoped>
/* (Styles are unchanged) */
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
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  width: 100%;
}
.event-title,
.event-date,
.event-location,
.event-description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #111;
}
.event-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
  white-space: nowrap;
}
.reminder-button {
  background-color: green;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.cancel-button {
  background-color: red;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
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
    fadeout 0.3s ease 2.7s;
}
.toast.error {
  background-color: #f44336;
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
