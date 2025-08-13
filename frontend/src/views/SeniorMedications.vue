<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useMedicationStore } from '../store/medicationStore';
import ScheduleRowItem from '../components/ScheduleRowItem.vue';
import MedicationForm from '../components/MedicationForm.vue';

const medicationStore = useMedicationStore();
const route = useRoute();
// Ensure seniorId is consistently available
const seniorId = route.params.id;

const toastMessage = ref('');
const showModal = ref(false);
const selectedMedication = ref(null);
const isEdit = ref(false);

const medications = computed(() => medicationStore.medications);
const loading = computed(() => medicationStore.loading);
const error = computed(() => medicationStore.error);

onMounted(() => {
  medicationStore.fetchMedications(seniorId);
});

function addMedications() {
  selectedMedication.value = null;
  isEdit.value = false;
  showModal.value = true;
}

function editMedications(item) {
  selectedMedication.value = { ...item };
  isEdit.value = true;
  showModal.value = true;
}

async function deleteMedication(item) {
  if (confirm(`Are you sure you want to delete "${item.name}"?`)) {
    try {
      await medicationStore.deleteMedication(item.medication_id, seniorId);
      showToast(`Deleted: "${item.name}"`);
    } catch (err) {
      showToast(`Error deleting medication: ${err.message}`, 'error');
    }
  }
}

async function markAsTaken(item) {
  try {
    const payload = { isTaken: true };
    // Pass seniorId to the update action
    await medicationStore.updateMedication(item.medication_id, payload, seniorId);
    showToast(`Marked "${item.name}" as taken`);
  } catch (err) {
    showToast(`Error updating medication: ${err.message}`, 'error');
  }
}

async function handleFormSubmit(medicationData) {
  // Exclude fields that shouldn't be in the main payload for update
  const { medication_id, senior_id, ...payload } = medicationData;
  payload.time = new Date(payload.time).toISOString();

  try {
    if (isEdit.value) {
      await medicationStore.updateMedication(selectedMedication.value.medication_id, payload, seniorId);
      showToast(`Updated: "${payload.name || selectedMedication.value.name}"`);
    } else {
      await medicationStore.addMedication(payload, seniorId);
      showToast(`Added: "${payload.name}"`);
    }
    showModal.value = false;
  } catch (err) {
    showToast(`Error saving medication: ${err.message}`, 'error');
  }
}

function showToast(message, type = 'success') {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 3000);
}
</script>

<template>
  <div class="medications">
    <h1 style="text-align: center">My Medications</h1>
  </div>

  <div v-if="loading" class="loading">Loading medications...</div>

  <div v-else-if="error" class="error">
    {{ error }}
  </div>

  <div v-else-if="medications.length === 0" class="empty">No medications scheduled.</div>

  <div v-else class="med-schedule-list">
    <ScheduleRowItem
      v-for="med in medications"
      :key="med.medication_id"
      :schedule="med"
      :hide-type="true"
      :compact-layout="true"
    >
      <button v-if="!med.isTaken" class="mark-as-taken-button" @click="markAsTaken(med)">Mark as taken</button>
      <span v-else class="taken-status">Taken</span>
      <button class="edit-button" @click="editMedications(med)">Edit</button>
      <button class="delete-button" @click="deleteMedication(med)">Delete</button>
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
  color: #666; /* Changed for better visibility on light backgrounds */
}

.error {
  color: #e74c3c;
}

button {
  /* General button style */
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  margin: 0 4px;
}

.edit-button {
  background-color: #3498db; /* Blue */
}

.mark-as-taken-button {
  background-color: #2ecc71; /* Green */
}

.taken-status {
  color: #2ecc71;
  font-weight: bold;
  margin: 0 1rem;
}

.add-button {
  margin-top: 15px;
  display: block; /* Center the button */
  margin-left: auto;
  margin-right: auto;
  background-color: #1abc9c; /* Teal */
  width: 200px;
}

.delete-button {
  background-color: #e74c3c; /* Red */
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
    fadeout 0.3s ease 2.7s;
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
