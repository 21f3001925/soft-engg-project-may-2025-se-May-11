<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import appointmentService from '../services/appointmentService.js';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';

const route = useRoute();
const seniorId = parseInt(route.params.id);

const toastMessage = ref('');
const appointments = ref([]);
const loading = ref(false);
const error = ref(null);
const showForm = ref(false);
const editingId = ref(null);
const formData = ref({
  title: '',
  date_time: '',
  location: '',
});

// Fetch appointments for this senior
async function getAppointments() {
  loading.value = true;
  error.value = null;
  try {
    const res = await appointmentService.getAppointments({ params: { senior_id: seniorId } });
    const data = Array.isArray(res.data) ? res.data : [];
    appointments.value = data.map((appt) => ({
      id: appt.appointment_id,
      title: appt.title,
      date_time: appt.date_time,
      location: appt.location,
      senior_id: appt.senior_id,
      type: appt.type || 'appointment',
    }));
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Failed to load appointments';
  } finally {
    loading.value = false;
  }
}

onMounted(getAppointments);

// Open add form
function openAddForm() {
  editingId.value = null;
  formData.value = { title: '', date_time: '', location: '' };
  showForm.value = true;
}

// Open edit form
function editAppointment(item) {
  editingId.value = item.id;
  formData.value = {
    title: item.title,
    date_time: toInputDatetime(item.date_time),
    location: item.location || '',
  };
  showForm.value = true;
}

// Delete appointment
async function cancelAppointment(item) {
  try {
    await appointmentService.deleteAppointment(item.id);
    appointments.value = appointments.value.filter((i) => i.id !== item.id);
    showToast(`Cancelled: "${item.title}"`);
  } catch {
    showToast('Failed to cancel appointment');
  }
}

// Add or update appointment
async function submitAppointment() {
  try {
    // Only send the fields backend expects
    const payload = { ...formData.value };
    delete payload.reminder_time; // remove any extra field if present

    if (editingId.value) {
      // Update appointment
      await appointmentService.updateAppointment(editingId.value, payload);
      showToast('Appointment updated');
    } else {
      // Add appointment
      await appointmentService.addAppointment(payload);
      showToast('Appointment added');
    }

    showForm.value = false;
    resetForm();
    await getAppointments(); // refresh list
  } catch (err) {
    console.error('Save failed:', err.response?.data || err.message);
    showToast('Failed to save appointment');
  }
}

// Reset form after submit
function resetForm() {
  editingId.value = null;
  formData.value = { title: '', date_time: '', location: '' };
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}

// Helper: convert API datetime to input type datetime-local format
function toInputDatetime(dateTimeStr) {
  const d = new Date(dateTimeStr);
  const tzOffset = d.getTimezoneOffset() * 60000;
  return new Date(d - tzOffset).toISOString().slice(0, 16);
}
</script>

<template>
  <div class="appointments">
    <h1>Appointments</h1>

    <div v-if="loading" class="loading">Loading appointments...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="appointments.length === 0" class="empty">No appointments scheduled</div>

    <!-- Appointment list -->
    <div v-else class="appointment-list">
      <ScheduleRowItem
        v-for="item in appointments"
        :key="item.id"
        :schedule="item"
        :hide-type="true"
        :compact-layout="true"
      >
        <div class="flex flex-col gap-1 w-full">
          <div class="font-semibold">{{ item.title }}</div>
          <div class="text-sm text-gray-600">
            <strong>Date:</strong>
            {{ new Date(item.date_time).toLocaleDateString() }}
          </div>
          <div class="text-sm text-gray-600" v-if="item.location"><strong>Location:</strong> {{ item.location }}</div>

          <div class="flex gap-2 mt-2">
            <button class="cancel-button" @click="cancelAppointment(item)">Delete</button>
            <button class="edit-button" @click="editAppointment(item)">Edit</button>
          </div>
        </div>
      </ScheduleRowItem>
    </div>

    <!-- Action buttons -->
    <div class="action-bar">
      <button class="add-button" @click="openAddForm">Add Appointment</button>
    </div>

    <!-- Add / Update form -->
    <div v-if="showForm" class="form-popup p-6 bg-white rounded-xl shadow-md max-w-md mx-auto">
      <h3 class="text-xl font-semibold mb-4">
        {{ editingId ? 'Edit Appointment' : 'Add Appointment' }}
      </h3>
      <form @submit.prevent="submitAppointment" class="space-y-4">
        <input
          v-model="formData.title"
          placeholder="Title"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-black"
        />
        <input
          v-model="formData.date_time"
          type="datetime-local"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-black"
        />
        <input
          v-model="formData.location"
          placeholder="Location (optional)"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-black"
        />

        <div class="form-actions flex justify-end space-x-3 mt-4">
          <button
            type="submit"
            class="px-5 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700 transition"
          >
            {{ editingId ? 'Update' : 'Save' }}
          </button>
          <button
            type="button"
            @click="showForm = false"
            class="px-5 py-2 rounded-md bg-red-500 text-white hover:bg-red-700 transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Toast -->
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
