<script setup>
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useScheduleStore } from '../store/scheduleStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import { useCaregiverStore } from '../store/caregiverStore';

const scheduleStore = useScheduleStore();
const caregiverStore = useCaregiverStore();

const route = useRoute();
const seniorId = parseInt(route.params.id);

onMounted(async () => {
  await scheduleStore.fetchAllMedications();
  console.log('Fetched Medications:', JSON.stringify(scheduleStore.allMedications.items, null, 2));
});

const medications = computed(() => scheduleStore.allMedications.items.filter((med) => med.id === seniorId));

const seniorName = computed(() => {
  const senior = caregiverStore.assignedSeniors.find((s) => s.id === seniorId);
  return senior ? senior.name : 'Senior';
});

function editMedications() {
  console.log('Edit button clicked!');
}

function markAsTaken() {
  console.log('Mark as taken button clicked!');
}

function addMedications() {
  console.log('Add medication button clicked!');
}

function deleteMedication() {
  console.log('Delete medication button clicked!');
}
</script>

<template>
  <div class="medications">
    <h1 style="text-align: center">{{ seniorName }}'s Medications</h1>
  </div>

  <div v-if="scheduleStore.schedule.loading" class="loading">Loading medications...</div>

  <div v-else-if="scheduleStore.schedule.error" class="error">
    {{ scheduleStore.schedule.error }}
  </div>

  <div v-else-if="medications.length === 0" class="empty">No medications for today</div>

  <div v-else class="med-schedule-list">
    <ScheduleRowItem
      v-for="schedule in medications"
      :key="schedule.id"
      :schedule="schedule"
      :hide-type="true"
      :compact-layout="true"
    >
      <button class="mark-as-taken-button" @click="markAsTaken(schedule)">Mark as taken</button>
      <button class="edit-button" @click="editMedications(schedule)">Edit</button>
      <button class="delete-button" @click="deleteMedication(schedule)">Delete</button>
    </ScheduleRowItem>
  </div>

  <div>
    <button class="add-button" @click="addMedications(schedule)">Add Medication</button>
    <div></div>
  </div>
</template>

<style scoped>
.medication-style {
  color: #1480be;
  font-weight: bold;
  font-size: 1.2rem;
}

.medications {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.medications h1 {
  margin-bottom: 2rem;
  color: #1480be;
  font-size: 2rem;
  margin-top: 1px;
}

.med-stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.med-schedule-list {
  display: flex;
  flex-direction: column;
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem;
  color: #f5f5f5;
}

.error {
  color: #e74c3c;
}

.edit-button {
  background-color: blueviolet;
}

.mark-as-taken-button {
  background-color: green;
}

.add-button {
  margin-top: 15px;
  margin-left: 236px;
  background-color: rgb(81, 188, 231);
  text-decoration-color: black;
}

.delete-button {
  background-color: red;
}

.schedule-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
