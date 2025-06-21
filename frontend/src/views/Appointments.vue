<script setup>
import { onMounted, computed } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';

const scheduleStore = useScheduleStore();

onMounted(async () => {
  await scheduleStore.fetchSchedules();
});

const appointments = computed(() =>
  scheduleStore.schedule.items.filter(item => item.type === 'appointment')
);

function editAppointment(item) {
  console.log('Edit appointment button:', item);
}

function cancelAppointment(item) {
  console.log('Cancel appointment button:', item);
}

function addAppointment() {
  console.log('Add new appointment button');
}
</script>

<template>
  <div class="appointments">
    <h1>Your Appointments</h1>

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
        :hideType="true"
        :compactLayout="true"
      >
        <button @click="editAppointment(item)" class="edit-button">Edit</button>
        <button @click="cancelAppointment(item)" class="cancel-button">Cancel</button>
      </ScheduleRowItem>
    </div>

    <div class="action-bar">
      <button @click="addAppointment" class="add-button">Add Appointment</button>
    </div>
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
</style>