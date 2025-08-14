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
  reminder_time: '',
});

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

// Add or update appointment
async function submitAppointment() {
  try {
    // Copy formData without reminder_time
    const payload = { ...formData.value };
    delete payload.reminder_time;

    if (editingId.value) {
      // Pass the ID and filtered data separately
      await appointmentService.updateAppointment(
        editingId.value, // just the ID
        payload, // no reminder_time
      );
      showToast('Appointment updated');
    } else {
      await appointmentService.addAppointment(payload);
      showToast('Appointment added');
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

// Edit appointment
function editAppointment(item) {
  editingId.value = item.id;
  formData.value = {
    title: item.name,
    date_time: item.date_time,
    location: item.location,
    reminder_time: item.reminder_time || null, //
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

    <!-- Appointment list -->
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

          <!-- Show date & time only here, not inside ScheduleRowItem -->
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

    <!-- Action buttons -->
    <div class="action-bar">
      <button class="add-button" @click="showForm = true">Add Appointment</button>
      <button class="add-button" @click="goToeventsPage">Explore Events</button>
    </div>

    <!-- Small add/update form -->
    <div v-if="showForm" class="form-popup p-6 bg-black rounded-xl shadow-md max-w-md mx-auto">
      <h3 class="text-xl font-semibold mb-4 text-white-800">
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
          placeholder="Location"
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
  </div>

  <!-- Toast -->
  <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
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
}
.edit-button {
  background-color: #0984e3;
  color: white;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
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
  gap: 1rem;
}
.form-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  width: 8cm;
  height: auto;
}
.form-popup input {
  width: 100%;
  padding: 0.4rem;
  margin-bottom: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-actions {
  display: flex;
  justify-content: space-between;
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
