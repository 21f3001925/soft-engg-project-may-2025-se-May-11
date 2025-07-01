<script setup>
import { computed } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';

const scheduleStore = useScheduleStore();

function toggleMedication(id) {
  const med = scheduleStore.medications.find((m) => m.id === id);
  if (med) {
    med.taken = !med.taken;
  }
}

const completedMeds = computed(() => scheduleStore.medications.filter((med) => med.taken).length);
const totalMeds = computed(() => scheduleStore.medications.length);
const progressPercentage = computed(() => (totalMeds.value === 0 ? 0 : (completedMeds.value / totalMeds.value) * 100));
</script>

<template>
  <div style="margin-bottom: 2rem">
    <h3>Medications</h3>
    <div style="margin-bottom: 0.5rem">
      <span>{{ completedMeds }}/{{ totalMeds }} taken</span>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
      </div>
    </div>
    <ul>
      <li
        v-for="med in scheduleStore.medications"
        :key="med.id"
        style="display: flex; align-items: center; margin-bottom: 0.5rem"
      >
        <input type="checkbox" :id="'med-' + med.id" :checked="med.taken" @change="toggleMedication(med.id)" />
        <label :for="'med-' + med.id" style="margin-left: 0.5rem">{{ med.name }} ({{ med.time }})</label>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.progress-bar-container {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  margin-top: 4px;
}
.progress-bar {
  background: #4f8cff;
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}
</style>
