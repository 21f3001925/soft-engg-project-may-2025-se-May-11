<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useMedicationStore } from '../store/medicationStore';
// --- 1. IMPORT THE CORRECT, NEW COMPONENT ---
import MedScheduleRowItem from '../components/MedScheduleRowItem.vue';
import MedicationForm from '../components/MedicationForm.vue';

const medicationStore = useMedicationStore();
const route = useRoute();
const seniorId = route.params.id;

// --- 2. THIS VIEW IS ALWAYS THE CAREGIVER'S VIEW ---
const isCaregiverView = true;

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

function editMedications(item) {
  selectedMedication.value = { ...item };
  isEdit.value = true;
  showModal.value = true;
}

async function deleteMedication(item) {
  if (confirm(`Are you sure you want to delete "${item.name}"?`)) {
    await medicationStore.deleteMedication(item.medication_id, seniorId);
    showToast(`Deleted: "${item.name}"`);
  }
}

async function handleFormSubmit(medicationData) {
  const { medication_id, ...payload } = medicationData;
  // payload.time = new Date(payload.time).toISOString();

  if (isEdit.value) {
    await medicationStore.updateMedication(selectedMedication.value.medication_id, payload, seniorId);
    showToast(`Updated: "${payload.name || selectedMedication.value.name}"`);
  } else {
    // Caregivers can add medications for seniors
    await medicationStore.addMedication(payload, seniorId);
    showToast(`Added: "${payload.name}"`);
  }
  showModal.value = false;
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 3000);
}
</script>

<template>
  <div class="medications">
    <h1>Caregiver View: Senior's Medications</h1>
  </div>

  <div v-if="loading" class="loading">Loading medications...</div>
  <div v-else-if="error" class="error">{{ error }}</div>
  <div v-else-if="medications.length === 0" class="empty">No medications scheduled.</div>

  <div v-else class="med-schedule-list">
    <MedScheduleRowItem
      v-for="med in medications"
      :key="med.medication_id"
      :schedule="med"
      :is-caregiver-view="isCaregiverView"
      @edit="editMedications"
      @delete="deleteMedication"
    />
  </div>

  <div>
    <button
      class="add-button"
      @click="
        () => {
          isEdit = false;
          selectedMedication = null;
          showModal = true;
        }
      "
    >
      Add Medication
    </button>
  </div>

  <<MedicationForm
    v-if="showModal"
    :model-value="selectedMedication"
    :is-edit="isEdit"
    @submit="handleFormSubmit"
    @close="showModal = false"
    :is-caregiver-view="isCaregiverView"
  />

  <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
</template>

<style scoped>
/* Styles are simplified because row-item styles are in the component now */
.medications {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.medications h1 {
  margin-bottom: 2rem;
  color: #1480be;
  font-size: 2rem;
  text-align: center;
}

.med-schedule-list {
  display: flex;
  flex-direction: column;
  background-color: #fff;
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
  color: #666;
}

.error {
  color: #e74c3c;
}

.add-button {
  margin-top: 15px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  background-color: #1abc9c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
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
