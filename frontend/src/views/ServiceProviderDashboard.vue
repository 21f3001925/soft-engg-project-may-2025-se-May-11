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
  <div class="dashboard service-provider-dashboard max-w-7xl mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
      <div class="col-span-1 md:col-span-3">
        <div
          class="flex items-center justify-between mb-8 p-6 rounded-2xl shadow bg-gradient-to-r from-purple-100 via-white to-pink-100 border border-purple-50"
        >
          <div>
            <h2
              class="dashboard-title text-2xl md:text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-1"
            >
              Manage Local Events
            </h2>
            <p class="text-xs text-gray-500 hidden md:block">Create and manage events for the community</p>
          </div>

          <div class="flex items-center space-x-2 bg-white/80 rounded-full px-4 py-2 shadow border border-gray-100">
            <span class="text-lg font-mono text-gray-700">{{
              new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }}</span>
          </div>
        </div>
      </div>

      <div class="col-span-1 md:col-span-3">
        <div v-if="providerStore.loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <span class="ml-3 text-gray-600">Loading events...</span>
        </div>

        <div v-else-if="providerStore.error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
          <div class="text-red-600 text-lg font-semibold mb-2">Error Loading Events</div>
          <div class="text-red-500">{{ providerStore.error }}</div>
        </div>

        <div v-else-if="events.length === 0" class="text-center py-16">
          <div
            class="w-24 h-24 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg"
          >
            <svg class="w-12 h-12 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              ></path>
            </svg>
          </div>
          <h3 class="text-2xl font-semibold text-gray-900 mb-3">No Events Scheduled</h3>
          <p class="text-gray-600 mb-8 max-w-md mx-auto">
            You don't have any events scheduled yet. Create your first event to get started!
          </p>
          <button
            @click="openAddModal"
            class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              ></path>
            </svg>
            Create First Event
          </button>
        </div>

        <div v-else class="space-y-6">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6">
              <ScheduleRowItem
                v-for="item in events"
                :key="item.event_id || item.id"
                :schedule="item"
                class="mb-4 last:mb-0"
              >
                <div class="flex gap-2">
                  <button
                    class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium"
                    @click="openEditModal(item)"
                  >
                    Edit
                  </button>
                  <button
                    class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
                    @click="deleteEvent(item)"
                  >
                    Delete
                  </button>
                  <button
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                    @click="openAttendeesModal(item)"
                  >
                    Show Attendees
                  </button>
                </div>
              </ScheduleRowItem>
            </div>
          </div>

          <div class="flex justify-center">
            <button
              @click="openAddModal"
              class="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
            >
              Add New Event
            </button>
          </div>
        </div>
      </div>
    </div>

    <EventForm
      v-if="showModal"
      :model-value="selectedItem"
      :is-edit="isEdit"
      @submit="handleFormSubmit"
      @close="showModal = false"
    />

    <div v-if="toastMessage" class="fixed top-4 right-4 z-50">
      <div class="bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
        {{ toastMessage }}
      </div>
    </div>

    <!-- Attendees Modal -->
    <div
      v-if="showAttendeesModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeAttendeesModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-900">Event Information and Attendees</h3>
            <button @click="closeAttendeesModal" class="text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <h4 class="font-semibold text-gray-900 mb-3">Event Details</h4>
            <div class="space-y-2 text-gray-700">
              <div><strong>Name:</strong> {{ modalEvent?.name }}</div>
              <div><strong>Date:</strong> {{ formatFullDateTime(modalEvent?.date_time) }}</div>
              <div><strong>Location:</strong> {{ modalEvent?.location }}</div>
              <div><strong>Description:</strong> {{ modalEvent?.description }}</div>
            </div>
          </div>

          <div>
            <h4 class="font-semibold text-gray-900 mb-3">Attendees</h4>
            <div v-if="attendeesForEvent.length === 0" class="text-gray-500 text-center py-4">No attendees yet</div>
            <div v-else class="space-y-2">
              <div
                v-for="senior in attendeesForEvent"
                :key="senior.user_id"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <span class="text-gray-700">{{ senior.name }} ({{ senior.email }})</span>
                <button
                  class="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600 transition-colors"
                  @click="removeAttendeeFromEvent(senior)"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>

          <div class="flex justify-end mt-6">
            <button
              @click="closeAttendeesModal"
              class="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
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

.dashboard-title {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
}
</style>
