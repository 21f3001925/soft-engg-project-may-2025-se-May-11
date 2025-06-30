<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useScheduleStore } from '../store/scheduleStore';
import { useCaregiverStore } from '../store/caregiverStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import MedicationForm from '../components/MedicationForm.vue';

const scheduleStore = useScheduleStore();
const caregiverStore = useCaregiverStore();

const route = useRoute();
const seniorId = parseInt(route.params.id);

const toastMessage = ref('');
const selectedMedication = ref(null);
const isEdit = ref(false);
const showModal = ref(false);

onMounted(async () => {
  await scheduleStore.fetchAllMedications();
});

const medications = computed(() => scheduleStore.allMedications.items.filter((med) => med.id === seniorId));

const seniorName = computed(() => {
  const senior = caregiverStore.assignedSeniors.find((s) => s.id === seniorId);
  return senior ? senior.name : 'Senior';
});

function addMedications() {
  selectedMedication.value = null;
  isEdit.value = false;
  showModal.value = true;
}

function editMedications(item) {
  selectedMedication.value = item;
  isEdit.value = true;
  showModal.value = true;
}

function deleteMedication(item) {
  scheduleStore.allMedications.items = scheduleStore.allMedications.items.filter((m) => m.id !== item.id);
  showToast(`Deleted: "${item.name}"`);
}

function markAsTaken(item) {
  item.taken = true;
  showToast(`Marked "${item.name}" as taken`);
}

function handleFormSubmit(medication) {
  if (isEdit.value) {
    const index = scheduleStore.allMedications.items.findIndex((m) => m.id === medication.id);
    if (index !== -1) {
      scheduleStore.allMedications.items[index] = { ...medication };
      showToast(`Updated: "${medication.name}"`);
    }
  } else {
    scheduleStore.allMedications.items.push({
      ...medication,
      id: Date.now(), // mock ID
      type: 'medication',
    });
    showToast(`Added: "${medication.name}"`);
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
    <button class="add-button" @click="addMedications">Add Medication</button>
  </div>

  <MedicationForm
    v-if="showModal"
    :model-value="selectedMedication"
    :is-edit="isEdit"
    @submit="handleFormSubmit"
    @close="showModal = false"
  />

  <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
</template>

<style scoped>
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

.med-schedule-list {
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
}

.delete-button {
  background-color: red;
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
