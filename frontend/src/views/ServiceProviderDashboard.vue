<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProviderStore } from '../store/providerStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue'; // Uses the corrected component
import EventForm from '../components/EventForm.vue';

const providerStore = useProviderStore();
const selectedItem = ref(null);
const showModal = ref(false);
const isEdit = ref(false);
const toastMessage = ref('');
const showAttendeesModal = ref(false);
const attendeesForEvent = ref([]);
const modalEvent = ref(null);

onMounted(async () => {
  await providerStore.fetchEvents();
});

const events = computed(() => providerStore.events || []);
const attendees = computed(() => providerStore.attendees || {});

function formatFullDateTime(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  };
  return date.toLocaleString('en-US', options);
}

function openAddModal() {
  selectedItem.value = null;
  isEdit.value = false;
  showModal.value = true;
}

function openEditModal(item) {
  selectedItem.value = { ...item };
  isEdit.value = true;
  showModal.value = true;
}

async function deleteEvent(item) {
  try {
    await providerStore.deleteEvent(item.event_id || item.id);
    showToast(`Deleted: "${item.name}"`);
  } catch (err) {
    showToast('Failed to delete event');
  }
}

async function handleFormSubmit(eventData) {
  try {
    if (isEdit.value) {
      await providerStore.updateEvent(selectedItem.value.event_id || selectedItem.value.id, eventData);
      showToast(`Updated: "${eventData.name}"`);
    } else {
      await providerStore.addEvent(eventData);
      showToast(`Added new event: "${eventData.name}"`);
    }
    showModal.value = false;
  } catch (err) {
    showToast('Failed to save event');
  }
}

function showToast(msg) {
  toastMessage.value = msg;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}

async function openAttendeesModal(event) {
  if (!attendees.value[event.event_id]) {
    await providerStore.fetchEventAttendees(event.event_id);
  }
  attendeesForEvent.value = attendees.value[event.event_id] || [];
  modalEvent.value = event;
  showAttendeesModal.value = true;
}

function closeAttendeesModal() {
  showAttendeesModal.value = false;
  attendeesForEvent.value = [];
  modalEvent.value = null;
}

async function removeAttendeeFromEvent(senior) {
  if (!modalEvent.value) return;
  try {
    await providerStore.removeAttendee(modalEvent.value.event_id, senior.user_id);
    showToast(`Removed ${senior.name || senior.email} from event`);
    attendeesForEvent.value = providerStore.attendees[modalEvent.value.event_id] || [];
  } catch (err) {
    showToast(providerStore.error || 'Failed to remove attendee');
  }
}
</script>

<template>
  <div class="dashboard-container">
    <h1>Manage Local Events</h1>

    <div v-if="providerStore.loading" class="loading">Loading events...</div>
    <div v-else-if="providerStore.error" class="error">
      {{ providerStore.error }}
    </div>
    <div v-else-if="events.length === 0" class="empty">No events scheduled. Add one below!</div>

    <div v-else class="list-container">
      <ScheduleRowItem v-for="item in events" :key="item.event_id || item.id" :schedule="item">
        <button class="edit-button" @click="openEditModal(item)">Edit</button>
        <button class="cancel-button" @click="deleteEvent(item)">Delete</button>
        <button class="attendees-button" @click="openAttendeesModal(item)">Show Attendees</button>
      </ScheduleRowItem>
    </div>

    <div class="action-bar">
      <button class="add-button" @click="openAddModal">Add New Event</button>
    </div>

    <EventForm
      v-if="showModal"
      :model-value="selectedItem"
      :is-edit="isEdit"
      @submit="handleFormSubmit"
      @close="showModal = false"
    />

    <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>

    <div v-if="showAttendeesModal" class="modal-overlay" @click.self="closeAttendeesModal">
      <div class="modal-content">
        <h2><b>Event Information and Attendees</b></h2>
        <div class="event-details">
          <div>Name: {{ modalEvent?.name }}</div>
          <div>Date: {{ formatFullDateTime(modalEvent?.date_time) }}</div>
          <div>Location: {{ modalEvent?.location }}</div>
          <div>Description: {{ modalEvent?.description }}</div>
        </div>
        <h3><strong>Attendees:</strong></h3>
        <ul>
          <li
            v-for="senior in attendeesForEvent"
            :key="senior.user_id"
            style="display: flex; align-items: center; gap: 0.5rem"
          >
            <span>{{ senior.name }} ({{ senior.email }})</span>
            <button class="remove-attendee-btn" @click="removeAttendeeFromEvent(senior)">Remove</button>
          </li>
          <li v-if="attendeesForEvent.length === 0">No attendees yet</li>
        </ul>
        <button class="close-modal" @click="closeAttendeesModal">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles from your original file will work here */
.dashboard-container {
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

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #ed240d;
}

.list-container {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto;
}

.edit-button {
  background-color: #6c5ce7;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
}

.cancel-button {
  background-color: #d63031;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
}

.add-button {
  background-color: #00cec9;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  color: white;
}

.action-bar {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
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

.attendees-button {
  background-color: #0984e3;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-content {
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 10px;
  min-width: 350px;
  max-width: 95vw;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.18);
  position: relative;
}

.close-modal {
  margin-top: 1.5rem;
  background: #d63031;
  color: #fff;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 5px;
  cursor: pointer;
}

.event-details {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.event-details > div {
  margin-bottom: 0.3rem;
}

.remove-attendee-btn {
  background: #d63031;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 2px 6px;
  margin-left: 8px;
  cursor: pointer;
  font-size: 0.85em;
  line-height: 1;
  height: 22px;
  min-width: 48px;
}
</style>
