<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import appointmentService from '../services/appointmentService.js';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';

const router = useRouter();
const toastMessage = ref('');
const loading = ref(false);
const error = ref(null);
const appointments = ref([]);

const showForm = ref(false);
const editingId = ref(null);
const formData = ref({
  title: '',
  date_time: '',
  location: '',
  reminder_time: '', // Field is already here, which is great
});

// Helper to format date string for datetime-local input
function toInputDatetime(dateString) {
  if (!dateString) return '';
  return dateString.slice(0, 16);
}

// Fetch from backend
async function getAppointments() {
  loading.value = true;
  error.value = null;
  try {
    const res = await appointmentService.getAppointments();
    if (Array.isArray(res.data)) {
      appointments.value = res.data.map((appt) => ({
        id: appt.appointment_id,
        name: appt.title,
        date_time: appt.date_time,
        location: appt.location,
        reminder_time: appt.reminder_time, // Make sure to get reminder_time from API
        type: 'appointment',
      }));
    } else {
      appointments.value = [];
    }
  } catch (err) {
    error.value = err.response?.data?.message || err.message;
  } finally {
    loading.value = false;
  }
}

// *** MODIFIED FUNCTION ***
// Add or update appointment
async function submitAppointment() {
  try {
    // Copy all form data into the payload
    const payload = {
      title: formData.value.title,
      date_time: formData.value.date_time,
      location: formData.value.location,
    };

    // If reminder_time is set, add it to the payload
    if (formData.value.reminder_time) {
      payload.reminder_time = formData.value.reminder_time;
    }

    if (editingId.value) {
      // **CHANGE**: Send the full payload, including reminder_time if present
      await appointmentService.updateAppointment(editingId.value, payload);
      showToast('Appointment and reminder updated');
    } else {
      // **CHANGE**: Send the full payload for new appointments
      await appointmentService.addAppointment(payload);
      showToast('Appointment and reminder added');
    }

    showForm.value = false;
    resetForm();
    await getAppointments();
  } catch (err) {
    showToast('Failed to save appointment');
    console.error(err);
  }
}

// Delete appointment
async function cancelAppointment(item) {
  try {
    await appointmentService.deleteAppointment(item.id);
    appointments.value = appointments.value.filter((i) => i.id !== item.id);
    showToast(`Cancelled: "${item.name}"`);
  } catch (err) {
    showToast('Failed to cancel appointment');
  }
}

// *** MODIFIED FUNCTION ***
// Edit appointment
function editAppointment(item) {
  editingId.value = item.id;
  formData.value = {
    title: item.name,
    // **CHANGE**: Use helper to format dates for the input fields
    date_time: toInputDatetime(item.date_time),
    location: item.location,
    reminder_time: toInputDatetime(item.reminder_time),
  };
  showForm.value = true;
}

function resetForm() {
  editingId.value = null;
  formData.value = { title: '', date_time: '', location: '', reminder_time: '' };
}

function goToeventsPage() {
  router.push('/events');
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}

onMounted(getAppointments);
</script>

<template>
  <div class="appointments">
    <h1>Your Appointments</h1>

    <div v-if="loading" class="loading">Loading appointments...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="appointments.length === 0" class="empty">No appointments scheduled</div>

    <div v-else class="appointment-list">
      <ScheduleRowItem
        v-for="item in appointments"
        :key="item.id"
        :schedule="item"
        :hide-type="true"
        :compact-layout="true"
      >
        <div class="flex flex-col gap-1">
          <div class="font-semibold">{{ item.title }}</div>
          <div class="text-sm text-gray-600">
            <strong>Date:</strong> {{ new Date(item.date_time).toLocaleDateString() }}
          </div>
          <div class="flex gap-2 mt-2">
            <button class="cancel-button" @click="cancelAppointment(item)">Cancel</button>
            <button class="edit-button" @click="editAppointment(item)">Edit</button>
          </div>
        </div>
      </ScheduleRowItem>
    </div>

    <div class="action-bar">
      <button class="add-button" @click="showForm = true">Add Appointment</button>
      <button class="add-button" @click="goToeventsPage">Explore Events</button>
    </div>

    <div v-if="showForm" class="form-popup p-6 bg-black rounded-xl shadow-md max-w-md mx-auto">
      <h3 class="text-xl font-semibold mb-4 text-white-800">
        {{ editingId ? 'Edit Appointment' : 'Add Appointment' }}
      </h3>
      <form @submit.prevent="submitAppointment" class="space-y-4">
        <label class="text-white">Title</label>
        <input v-model="formData.title" placeholder="Title" required class="form-input" />

        <label class="text-white">Date & Time</label>
        <input v-model="formData.date_time" type="datetime-local" required class="form-input" />

        <label class="text-white">Location</label>
        <input v-model="formData.location" placeholder="Location" class="form-input" />

        <label class="text-white">Reminder Time (Optional)</label>
        <input v-model="formData.reminder_time" type="datetime-local" class="form-input" />

        <div class="form-actions flex justify-end space-x-3 mt-4">
          <button type="submit" class="submit-button">
            {{ editingId ? 'Update' : 'Save' }}
          </button>
          <button type="button" @click="showForm = false" class="cancel-form-button">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
</template>

<style scoped>
/* Your existing styles are fine, just adding a class for the inputs */
.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  color: black;
}
.submit-button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #28a745; /* Green */
  color: white;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.cancel-form-button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #dc3545; /* Red */
  color: white;
  border: none;
  cursor: pointer;
}
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
  box-shadow: 0 2px 4px rgb(215, 213, 213);
  max-width: 1000px;
  margin: 0 auto;
}
.cancel-button {
  background-color: #d63031;
  color: white;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  border: none;
}
.edit-button {
  background-color: #0984e3;
  color: white;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  border: none;
}
.add-button {
  margin-top: 15px;
  background-color: #00cec9;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  color: white;
  border: none;
}
.action-bar {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  gap: 1rem;
}
.form-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #333; /* Darker background for the form */
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 450px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
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
}
</style>
