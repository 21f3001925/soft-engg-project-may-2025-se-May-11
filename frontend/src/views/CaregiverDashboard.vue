<script setup>
import { onMounted, ref } from 'vue';
import { useCaregiverStore } from '../store/caregiverStore';
import SeniorCard from '../components/SeniorCard.vue';

const caregiverStore = useCaregiverStore();
const loading = ref(true);

onMounted(async () => {
  await caregiverStore.fetchAssignedSeniors();
  loading.value = false;
});
</script>

<template>
  <div class="dashboard">
    <h1>Caregiver Dashboard</h1>

    <div v-if="loading" class="loading">Loading seniors...</div>
    <div v-else-if="caregiverStore.assignedSeniors.length === 0" class="empty">No seniors assigned to you.</div>

    <div v-else class="seniors-grid">
      <SeniorCard v-for="senior in caregiverStore.assignedSeniors" :key="senior.id" :senior="senior" />
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
  color: #2c3e50;
  text-align: center;
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
