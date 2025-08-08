<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProviderStore } from '../store/providerStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import EventForm from '../components/EventForm.vue';

const providerStore = useProviderStore();
const selectedItem = ref(null);
const showModal = ref(false);
const isEdit = ref(false);
const toastMessage = ref('');

onMounted(async () => {
  await providerStore.fetchEvents();
});

const events = computed(() => providerStore.events || []);

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
      await providerStore.updateEvent(eventData.event_id || eventData.id, eventData);
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
</script>

<template>
  <div class="appointments">
    <h1>Manage Local Events</h1>

    <div v-if="providerStore.loading" class="loading">Loading events...</div>
    <div v-else-if="providerStore.error" class="error">
      {{ providerStore.error }}
    </div>
    <div v-else-if="events.length === 0" class="empty">No events scheduled</div>

    <div v-else class="appointment-list">
      <ScheduleRowItem
        v-for="item in events"
        :key="item.event_id || item.id"
        :schedule="item"
        :hide-type="true"
        :compact-layout="true"
      >
        <button class="edit-button" @click="openEditModal(item)">Edit</button>
        <button class="cancel-button" @click="deleteEvent(item)">Delete</button>
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
  </div>
</template>

<style scoped>
.appointments {
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
  color: #f3ecec;
}

.error {
  color: #ed240d;
}

.appointment-list {
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
}

.cancel-button {
  background-color: #d63031;
}

.add-button {
  margin-top: 15px;
  background-color: #00cec9;
  padding: 0.5rem 1rem;
  border-radius: 4px;
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
</style>
