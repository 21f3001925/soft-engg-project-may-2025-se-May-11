<script setup>
import { useScheduleStore } from '../store/scheduleStore';

const scheduleStore = useScheduleStore();

function toggleMedication(id) {
  scheduleStore.medications = scheduleStore.medications.map((med) =>
    med.id === id ? { ...med, taken: !med.taken } : med,
  );
}
</script>

<template>
  <div style="margin-bottom: 2rem">
    <h3>Medications</h3>
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
