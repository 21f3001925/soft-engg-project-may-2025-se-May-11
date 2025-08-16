<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import appointmentService from '../services/appointmentService.js';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import { Calendar, Clock, MapPin, XCircle, AlertCircle } from 'lucide-vue-next';

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

function isOverdue(dateString) {
  if (!dateString) return false;
  const appointmentDate = new Date(dateString);
  const now = new Date();
  return appointmentDate < now;
}

function shouldShowOverdue(item) {
  // Don't show overdue for appointments that are already marked as Missed or Completed
  if (item.status === 'Missed' || item.status === 'Completed') {
    return false;
  }
  return isOverdue(item.date_time);
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
        status: appt.status || 'Scheduled',
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

async function completeAppointment(item) {
  try {
    await appointmentService.completeAppointment(item.id);
    const appointment = appointments.value.find((a) => a.id === item.id);
    if (appointment) {
      appointment.status = 'Completed';
    }
    showToast(`Completed: "${item.name}"`);
  } catch (err) {
    showToast('Failed to complete appointment');
    console.error(err);
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

function getStatusClass(status) {
  switch (status) {
    case 'Completed':
      return 'text-green-600 font-semibold';
    case 'Missed':
      return 'text-red-600 font-semibold';
    case 'Cancelled':
      return 'text-gray-500 font-semibold';
    default:
      return 'text-blue-600 font-semibold';
  }
}

onMounted(getAppointments);
</script>

<template>
  <div class="appointments min-h-screen bg-gradient-to-br from-gray-50 to-purple-50">
    <div class="max-w-6xl mx-auto px-6 py-8">
      <div class="mb-8">
        <h1 style="text-align: center; color: #1480be; font-size: 2rem; margin-bottom: 2rem; margin-top: 1px">
          Your Appointments
        </h1>
      </div>

      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        <span class="ml-3 text-gray-600">Loading appointments...</span>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 text-lg font-semibold mb-2">Error Loading Appointments</div>
        <div class="text-red-500">{{ error }}</div>
      </div>

      <div v-else-if="appointments.length === 0" class="text-center py-16">
        <div
          class="w-24 h-24 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg"
        >
          <Calendar class="w-12 h-12 text-purple-600" />
        </div>
        <h3 class="text-2xl font-semibold text-gray-700 mb-3">No Appointments Scheduled</h3>
        <p class="text-gray-500 mb-8 max-w-md mx-auto">
          You don't have any appointments scheduled yet. Create your first appointment to get started!
        </p>
        <button
          @click="showForm = true"
          class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
        >
          <Calendar class="w-5 h-5" />
          Schedule First Appointment
        </button>
      </div>

      <div v-else class="space-y-6">
        <div class="grid gap-6">
          <div
            v-for="item in appointments"
            :key="item.id"
            :class="[
              'bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden',
              shouldShowOverdue(item) ? 'border-red-200 bg-red-50/30' : '',
            ]"
          >
            <div class="p-6">
              <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-2">
                    <h3 class="text-xl font-semibold text-gray-900">{{ item.title }}</h3>
                    <span :class="getStatusClass(item.status)" class="px-3 py-1 rounded-full text-xs font-semibold">
                      {{ item.status }}
                    </span>
                    <span
                      v-if="shouldShowOverdue(item)"
                      class="px-3 py-1 bg-red-100 text-red-700 border border-red-200 rounded-full text-xs font-semibold flex items-center gap-1"
                    >
                      <AlertCircle class="w-3 h-3" />
                      Overdue
                    </span>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                    <div class="flex items-center gap-2">
                      <Calendar class="w-4 h-4 text-purple-500" />
                      <span><strong>Date:</strong> {{ new Date(item.date_time).toLocaleDateString() }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <Clock class="w-4 h-4 text-purple-500" />
                      <span
                        ><strong>Time:</strong>
                        {{
                          new Date(item.date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                        }}</span
                      >
                    </div>
                    <div class="flex items-center gap-2">
                      <MapPin class="w-4 h-4 text-purple-500" />
                      <span><strong>Location:</strong> {{ item.location }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex flex-wrap gap-3 mt-6">
                <button
                  v-if="item.status !== 'Completed'"
                  class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
                  @click="cancelAppointment(item)"
                >
                  Cancel
                </button>
                <button
                  v-if="item.status !== 'Completed'"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                  @click="editAppointment(item)"
                >
                  Edit
                </button>
                <button
                  v-if="item.status !== 'Completed'"
                  class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                  @click="completeAppointment(item)"
                >
                  Complete
                </button>
                <span v-else class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg font-medium"> Completed </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
        <button
          @click="showForm = true"
          class="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
        >
          Add New Appointment
        </button>
        <button
          @click="goToeventsPage"
          class="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-xl hover:from-blue-600 hover:to-indigo-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
        >
          Explore Events
        </button>
      </div>
    </div>

    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-900">
              {{ editingId ? 'Edit Appointment' : 'Add Appointment' }}
            </h3>
            <button @click="showForm = false" class="text-gray-400 hover:text-gray-600 transition-colors">
              <XCircle class="w-6 h-6" />
            </button>
          </div>

          <form @submit.prevent="submitAppointment" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
              <input
                v-model="formData.title"
                placeholder="Appointment title"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Date & Time</label>
              <input
                v-model="formData.date_time"
                type="datetime-local"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <input
                v-model="formData.location"
                placeholder="Appointment location"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Reminder Time (Optional)</label>
              <input
                v-model="formData.reminder_time"
                type="datetime-local"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
              />
            </div>

            <div class="flex gap-3 pt-4">
              <button
                type="submit"
                class="flex-1 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-200 font-semibold"
              >
                {{ editingId ? 'Update' : 'Save' }}
              </button>
              <button
                type="button"
                @click="showForm = false"
                class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-if="toastMessage" class="fixed top-4 right-4 z-50">
    <div class="bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
      {{ toastMessage }}
    </div>
  </div>
</template>

<style scoped>
/* Custom styles if needed */
</style>
