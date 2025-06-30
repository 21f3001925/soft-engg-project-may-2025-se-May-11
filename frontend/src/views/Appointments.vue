<script setup>
import { onMounted, computed, ref } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import { useRouter } from 'vue-router';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';

const scheduleStore = useScheduleStore();
const router = useRouter();
const toastMessage = ref('');

onMounted(async () => {
  await scheduleStore.fetchSchedules();
});

const appointments = computed(() =>
  scheduleStore.schedule.items.filter((item) => item.type === 'appointment' || item.type === 'event'),
);

function cancelAppointment(item) {
  scheduleStore.schedule.items = scheduleStore.schedule.items.filter((i) => i.id !== item.id);
  showToast(`Cancelled: "${item.name}"`);
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
</script>

<template>
  <div class="appointments">
    <h1>Your Appointments and Events</h1>

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
        <button class="cancel-button" @click="cancelAppointment(item)">Cancel</button>
      </ScheduleRowItem>
    </div>

    <div class="action-bar">
      <button class="add-button" @click="goToeventsPage">Explore Events</button>
    </div>
  </div>

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
