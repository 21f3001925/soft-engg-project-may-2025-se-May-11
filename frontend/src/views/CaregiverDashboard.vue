<script setup>
import { onMounted, ref } from 'vue';
import { useCaregiverStore } from '../store/caregiverStore';
import SeniorCard from '../components/SeniorCard.vue';

const caregiverStore = useCaregiverStore();
const loading = ref(true);
const selectedSenior = ref('');
const assignError = ref('');
const showAssignModal = ref(false);

onMounted(async () => {
  await caregiverStore.fetchAssignedSeniors();
  await caregiverStore.fetchAvailableSeniors();
  loading.value = false;
});

function openAssignModal() {
  showAssignModal.value = true;
  assignError.value = '';
  selectedSenior.value = '';
}

async function assignSenior() {
  if (!selectedSenior.value) return;
  assignError.value = '';
  try {
    await caregiverStore.assignCaregiverToSenior(selectedSenior.value);
    selectedSenior.value = '';
    showAssignModal.value = false;
    await caregiverStore.fetchAssignedSeniors();
    await caregiverStore.fetchAvailableSeniors();
  } catch (err) {
    assignError.value = err.response?.data?.message || err.message || 'Failed to assign caregiver';
  }
}
</script>

<template>
  <div class="dashboard">
    <h1>Caregiver Dashboard</h1>

    <div v-if="loading" class="loading">Loading seniors...</div>

    <!-- Assignment UI: show inline only if no seniors assigned -->
    <div v-if="!loading && caregiverStore.assignedSeniors.length === 0">
      <div class="assign-section">
        <h2>Assign yourself to a Senior Citizen</h2>
        <div v-if="caregiverStore.availableSeniors.length === 0" class="empty">
          No unassigned seniors available.
        </div>
        <div v-else>
          <select v-model="selectedSenior">
            <option disabled value="">Select a senior</option>
            <option v-for="senior in caregiverStore.availableSeniors" :key="senior.id" :value="senior.id">
              {{ senior.name }} ({{ senior.email }})
            </option>
          </select>
          <button @click="assignSenior" :disabled="!selectedSenior">Assign</button>
        </div>
        <div v-if="assignError" class="error">{{ assignError }}</div>
      </div>
    </div>

    <!-- "Assign another senior" button and modal, shown if at least one assigned -->
    <div v-if="caregiverStore.assignedSeniors.length > 0" class="assign-another">
      <button
        class="assign-another-btn"
        @click="openAssignModal"
      >
        Assign another senior
      </button>
    </div>

    <!-- Modal for assignment -->
    <div v-if="showAssignModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Assign yourself to another Senior Citizen</h2>
        <div v-if="caregiverStore.availableSeniors.length === 0" class="empty">
          No unassigned seniors available.
        </div>
        <div v-else>
          <select v-model="selectedSenior">
            <option disabled value="">Select a senior</option>
            <option v-for="senior in caregiverStore.availableSeniors" :key="senior.id" :value="senior.id">
              {{ senior.name }} ({{ senior.email }})
            </option>
          </select>
          <button @click="assignSenior" :disabled="!selectedSenior">Assign</button>
        </div>
        <button class="close-btn" @click="showAssignModal = false">Cancel</button>
        <div v-if="assignError" class="error">{{ assignError }}</div>
      </div>
    </div>

    <!-- Dashboard for assigned seniors -->
    <div v-if="caregiverStore.assignedSeniors.length > 0">
      <div class="seniors-grid">
        <SeniorCard
          v-for="senior in caregiverStore.assignedSeniors"
          :key="senior.id"
          :senior="senior"
          @remove="() => caregiverStore.removeCaregiverFromSenior(senior.id)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 1rem 2rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  margin-top: 0;
}

h1 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: rgb(82, 82, 255);
  text-align: center;
  font-size: 30px;
}

.assign-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.assign-section h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 22px;
  color: #333;
}

.assign-section select,
.assign-section button {
  padding: 0.5rem;
  font-size: 16px;
}

.assign-section button {
  margin-left: 0.5rem;
  background-color: rgb(82, 82, 255);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.assign-section button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.assign-another {
  margin-bottom: 1.5rem;
  text-align: right;
}

.assign-another-btn {
  background-color: rgb(82, 82, 255);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 16px;
}

.error {
  color: red;
  margin-top: 0.5rem;
}

.seniors-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Always two cards per row */
  gap: 1.5rem;
  margin-top: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty {
  text-align: center;
  padding: 1rem;
  color: #666;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  min-width: 320px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.close-btn {
  background: #eee;
  color: #333;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 16px;
}
</style>
