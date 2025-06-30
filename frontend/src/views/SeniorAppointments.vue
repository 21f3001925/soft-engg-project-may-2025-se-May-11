<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useScheduleStore } from '../store/scheduleStore';
import { useCaregiverStore } from '../store/caregiverStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import EventForm from '../components/EventForm.vue';

const scheduleStore = useScheduleStore();
const caregiverStore = useCaregiverStore();
const route = useRoute();

const seniorId = parseInt(route.params.id);
const toastMessage = ref('');
const selectedAppointment = ref(null);
const isEdit = ref(false);
const showModal = ref(false);

onMounted(async () => {
  await scheduleStore.fetchSchedules();
});

const appointments = computed(() =>
  scheduleStore.schedule.items.filter(
    (item) => (item.type === 'appointment' || item.type === 'event') && item.id === seniorId,
  ),
);

const seniorName = computed(() => {
  const senior = caregiverStore.assignedSeniors.find((s) => s.id === seniorId);
  return senior ? senior.name : 'Senior';
});

function editAppointment(item) {
  selectedAppointment.value = { ...item };
  isEdit.value = true;
  showModal.value = true;
}

function cancelAppointment(item) {
  scheduleStore.schedule.items = scheduleStore.schedule.items.filter((i) => i !== item);
  showToast(`Cancelled: "${item.name}"`);
}

function addAppointment() {
  selectedAppointment.value = null;
  isEdit.value = false;
  showModal.value = true;
}

function handleFormSubmit(appointment) {
  if (isEdit.value) {
    const index = scheduleStore.schedule.items.findIndex((i) => i.id === appointment.id);
    if (index !== -1) {
      scheduleStore.schedule.items[index] = { ...appointment };
      showToast(`Updated: "${appointment.name}"`);
    }
  } else {
    scheduleStore.schedule.items.push({
      ...appointment,
      id: Date.now(), // mock ID
      type: 'appointment',
    });
    showToast(`Added: "${appointment.name}"`);
  }
  showModal.value = false;
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}
</script>

<template>
  <div class="appointments">
    <h1>{{ seniorName }} Appointments</h1>

    <div v-if="scheduleStore.schedule.loading" class="loading">Loading appointments...</div>

    <div v-else-if="scheduleStore.schedule.error" class="error">
      {{ scheduleStore.schedule.error }}
    </div>

    <div v-else-if="appointments.length === 0" class="empty">No appointments scheduled</div>

    <div v-else class="appointment-list">
      <ScheduleRowItem
        v-for="item in appointments"
        :key="item.id"
        :schedule="item"
        :hide-type="true"
        :compact-layout="true"
      >
        <button class="edit-button" @click="editAppointment(item)">Edit</button>
        <button class="cancel-button" @click="cancelAppointment(item)">Cancel</button>
      </ScheduleRowItem>
    </div>

    <div class="action-bar">
      <button class="add-button" @click="addAppointment">Add Appointment</button>
    </div>

    <EventForm
      v-if="showModal"
      :model-value="selectedAppointment"
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
