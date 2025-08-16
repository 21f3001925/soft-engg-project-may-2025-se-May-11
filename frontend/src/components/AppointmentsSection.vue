<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import { Calendar, ChevronRight, MapPin, Clock, Shield, CheckCircle, AlertCircle, XCircle } from 'lucide-vue-next';
import { getReminderTime } from '../services/timeutils.js';

const currentTime = ref(new Date());
const scheduleStore = useScheduleStore();
const appointments = computed(() =>
  scheduleStore.upcomingAppointments.slice(0, 5).map((appt) => ({
    ...appt,
    reminderLeft: getReminderTime(appt.reminder_time || appt.date_time, currentTime.value),
  })),
);

onMounted(() => {
  scheduleStore.getAppointments();
  const timer = setInterval(() => {
    currentTime.value = new Date();
  }, 60000);

  onUnmounted(() => {
    clearInterval(timer);
  });
});

async function completeAppointment(appointmentId) {
  try {
    await scheduleStore.completeAppointment(appointmentId);
    console.log('Appointment completed successfully');
  } catch (error) {
    console.error('Failed to complete appointment:', error);
  }
}

function getStatusBadgeClass(status) {
  switch (status) {
    case 'Completed':
      return 'bg-green-100 text-green-700 border border-green-200';
    case 'Missed':
      return 'bg-red-100 text-red-700 border border-red-200';
    case 'Cancelled':
      return 'bg-gray-100 text-gray-700 border border-gray-200';
    default:
      return 'bg-blue-100 text-blue-700 border border-blue-200';
  }
}

function getStatusIcon(status) {
  switch (status) {
    case 'Completed':
      return CheckCircle;
    case 'Missed':
      return AlertCircle;
    case 'Cancelled':
      return XCircle;
    default:
      return Clock;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  if (date.toDateString() === today.toDateString()) {
    return 'Today';
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Tomorrow';
  } else {
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
    });
  }
}

function isOverdue(dateString) {
  const appointmentDate = new Date(dateString);
  return appointmentDate < currentTime.value;
}

function shouldShowOverdue(appt) {
  // Don't show overdue for appointments that are already marked as Missed or Completed
  if (appt.status === 'Missed' || appt.status === 'Completed') {
    return false;
  }
  return isOverdue(appt.date_time);
}
</script>

<template>
  <div
    class="appointments-section mb-10 p-8 rounded-3xl shadow-xl border border-purple-100 bg-gradient-to-br from-white to-purple-50/30"
  >
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center text-2xl font-bold">
        <span
          class="w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 mr-4 shadow-lg"
        >
          <Calendar class="w-7 h-7 text-white" />
        </span>
        <span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent"> Appointments </span>
      </div>
    </div>

    <div v-if="appointments && appointments.length > 0" class="space-y-4">
      <div
        v-for="appt in appointments"
        :key="appt.id"
        :class="[
          'group relative p-6 bg-white rounded-2xl border border-gray-100 hover:border-purple-200 hover:shadow-lg transition-all duration-300 overflow-hidden',
          shouldShowOverdue(appt) ? 'border-red-200 bg-red-50/30' : '',
        ]"
      >
        <div
          class="absolute top-0 left-0 w-1 h-full"
          :class="
            shouldShowOverdue(appt)
              ? 'bg-gradient-to-b from-red-400 to-red-600'
              : 'bg-gradient-to-b from-purple-400 to-pink-400'
          "
        ></div>

        <div v-if="shouldShowOverdue(appt)" class="absolute top-4 right-4">
          <span
            class="px-3 py-1 bg-red-100 text-red-700 border border-red-200 rounded-full text-xs font-semibold flex items-center gap-1"
          >
            <AlertCircle class="w-3 h-3" />
            Overdue
          </span>
        </div>

        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-lg font-semibold text-gray-900 group-hover:text-purple-700 transition-colors">
                {{ appt.title }}
              </h3>
              <span
                v-if="appt.status !== 'Completed'"
                :class="getStatusBadgeClass(appt.status)"
                class="px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1"
              >
                <component :is="getStatusIcon(appt.status)" class="w-3 h-3" />
                {{ appt.status || 'Scheduled' }}
              </span>
            </div>

            <div class="flex items-center gap-4 text-sm text-gray-600">
              <div class="flex items-center gap-1">
                <Calendar class="w-4 h-4 text-purple-500" />
                <span class="font-medium">{{ formatDate(appt.date_time) }}</span>
              </div>
              <div class="flex items-center gap-1">
                <Clock class="w-4 h-4 text-purple-500" />
                <span class="font-medium">
                  {{ new Date(appt.date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2 mb-3">
          <MapPin class="w-4 h-4 text-gray-400" />
          <span class="text-sm text-gray-600">{{ appt.location }}</span>
        </div>

        <div
          v-if="appt.reminderLeft && appt.reminderLeft !== 'Overdue'"
          class="flex items-center gap-2 mb-4 p-3 bg-purple-50 rounded-lg"
        >
          <div class="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
          <span class="text-xs text-purple-700 font-medium"> Reminder: {{ appt.reminderLeft }} </span>
        </div>

        <div v-if="appt.status !== 'Completed'" class="flex justify-end">
          <button
            @click="completeAppointment(appt.id)"
            class="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white text-sm font-medium rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105"
          >
            <CheckCircle class="w-4 h-4" />
            Mark Complete
          </button>
        </div>
        <div v-else class="flex justify-end">
          <span
            class="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 text-sm font-medium rounded-lg"
          >
            <CheckCircle class="w-4 h-4" />
            Completed
          </span>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <div
        class="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg"
      >
        <Calendar class="w-10 h-10 text-purple-600" />
      </div>
      <h3 class="text-xl font-semibold text-gray-700 mb-3">No Upcoming Appointments</h3>
      <p class="text-gray-500 text-sm mb-6 max-w-md mx-auto">
        You don't have any appointments scheduled. Schedule your first appointment to get started!
      </p>
      <router-link
        to="/appointments"
        class="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105 font-medium"
      >
        Schedule Appointment
        <ChevronRight class="w-4 h-4" />
      </router-link>
    </div>

    <router-link
      to="/appointments"
      class="mt-8 w-full flex items-center justify-center gap-3 py-4 rounded-2xl bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 hover:from-purple-100 hover:to-pink-100 transition-all duration-300 text-purple-700 font-semibold shadow-sm hover:shadow-md hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-purple-300"
    >
      <span>View Full Calendar</span>
      <ChevronRight class="w-5 h-5" />
    </router-link>
  </div>
</template>
