<script setup>
import { onMounted, computed, ref } from 'vue';
import { useMedicationStore } from '../store/medicationStore';
import { useUserStore } from '../store/userStore'; // Import user store
import MedScheduleRowItem from '../components/MedScheduleRowItem.vue'; // Use our new component
import MedicationForm from '../components/MedicationForm.vue';

const medicationStore = useMedicationStore();
const userStore = useUserStore(); // Initialize user store

const toastMessage = ref('');

// Check if the current user is a caregiver
const isCaregiverView = computed(() => userStore.user?.roles?.includes('caregiver'));

onMounted(async () => {
  // Pass seniorId if caregiver is viewing
  const seniorId = isCaregiverView.value ? userStore.selectedSeniorId : null;
  await medicationStore.fetchMedications(seniorId);
});

const medications = computed(() => medicationStore.medications);

const showModal = ref(false);
const selectedMedication = ref(null);
const isEdit = ref(false);

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

async function deleteMedication(item) {
  await medicationStore.deleteMedication(item.medication_id);
  showToast(`Deleted "${item.name}"`);
}

async function markAsTaken(item) {
  await medicationStore.markAsTaken(item);
  showToast(`Marked "${item.name}" as taken`);
}

async function handleFormSubmit(formData) {
  try {
    // For "Edit" mode, the ID MUST come from the 'selectedMedication' ref,
    // because the form data doesn't contain the ID.
    if (isEdit.value && selectedMedication.value) {
      const medicationIdToUpdate = selectedMedication.value.medication_id;

      // Ensure the ID is valid before proceeding
      if (!medicationIdToUpdate) {
        throw new Error('Medication ID is missing. Cannot update.');
      }

      // The 'formData' is the payload from the form, which includes 'isTaken'
      const payload = { ...formData };

      // The parent component is responsible for converting the time format
      if (payload.time) {
        payload.time = new Date(payload.time).toISOString();
      }

      // 'seniorId' is null here, which is correct for the senior's own view
      await medicationStore.updateMedication(medicationIdToUpdate, payload, null);
      showToast(`Updated: "${payload.name || selectedMedication.value.name}"`);
    } else {
      // Logic for adding a new medication
      const payload = { ...formData };
      if (payload.time) {
        payload.time = new Date(payload.time).toISOString();
      }
      await medicationStore.addMedication(payload, null);
      showToast(`Added: "${payload.name}"`);
    }

    showModal.value = false;
  } catch (err) {
    showToast(`Error saving medication: ${err.message}`, 'error');
  }
}

function showToast(message) {
  toastMessage.value = message;
  setTimeout(() => {
    toastMessage.value = '';
  }, 2000);
}
</script>

<template>
  <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>

  <div class="medications">
    <h1 style="text-align: center">
      {{ isCaregiverView ? "Senior's Medications" : 'Your Medications' }}
    </h1>
  </div>

  <div v-if="medicationStore.loading" class="loading">Loading medications...</div>
  <div v-else-if="medicationStore.error" class="error">{{ medicationStore.error }}</div>
  <div v-else-if="medications.length === 0" class="empty">No medications scheduled.</div>

  <div v-else class="med-schedule-list">
    <MedScheduleRowItem
      v-for="schedule in medications"
      :key="schedule.medication_id"
      :schedule="schedule"
      :is-caregiver-view="isCaregiverView"
      @mark-as-taken="markAsTaken"
      @edit="editMedications"
      @delete="deleteMedication"
    />
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
</template>

<style scoped>
/* Scoped styles from your original file. The button styles are now in MedScheduleRowItem.vue */
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
  font-size: 1.2rem;
  color: #666;
}
.add-button {
  margin-top: 15px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  background-color: rgb(81, 188, 231);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
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
}
</style>
