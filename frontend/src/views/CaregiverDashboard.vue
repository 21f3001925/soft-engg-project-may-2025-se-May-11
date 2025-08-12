<script setup>
import { onMounted, ref, computed } from 'vue';
import { useCaregiverStore } from '../store/caregiverStore';
import SeniorCard from '../components/SeniorCard.vue';

const caregiverStore = useCaregiverStore();
const loading = ref(true);
const selectedSenior = ref('');
const assignError = ref('');

onMounted(async () => {
  await caregiverStore.fetchAssignedSeniors();
  await caregiverStore.fetchAvailableSeniors();
  loading.value = false;
});

const isAssigned = computed(() => caregiverStore.assignedSeniors.length > 0);

async function assignSenior() {
  assignError.value = '';
  try {
    await caregiverStore.assignCaregiverToSenior(selectedSenior.value);
    selectedSenior.value = '';
  } catch (err) {
    assignError.value = err.response?.data?.message || err.message || 'Failed to assign caregiver';
  }
}
</script>

<template>
  <div class="dashboard">
    <h1>Caregiver Dashboard</h1>

    <div v-if="loading" class="loading">Loading seniors...</div>

    <!-- Assignment UI -->
    <div v-else-if="!isAssigned">
      <div class="assign-section">
        <h2>Assign yourself to a Senior Citizen</h2>
        <select v-model="selectedSenior">
          <option disabled value="">Select a senior</option>
          <option v-for="senior in caregiverStore.availableSeniors" :key="senior.id" :value="senior.id">
            {{ senior.name }} ({{ senior.email }})
          </option>
        </select>
        <button @click="assignSenior" :disabled="!selectedSenior">Assign</button>
        <div v-if="assignError" class="error">{{ assignError }}</div>
        <div v-if="caregiverStore.availableSeniors.length === 0" class="empty">
          No unassigned seniors available.
        </div>
      </div>
    </div>

    <!-- Dashboard for assigned seniors -->
    <div v-else>
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

.error {
  color: red;
  margin-top: 0.5rem;
}

.seniors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 5rem;
}

.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
