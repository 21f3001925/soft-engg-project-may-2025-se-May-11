<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  med: {
    type: Object,
    required: true,
  },
  toggleMedication: {
    type: Function,
    required: true,
  },
});
</script>

<template>
  <li style="display: flex; align-items: center; margin-bottom: 0.5rem">
    <input type="checkbox" :id="'med-' + med.id" :checked="med.taken" @change="() => toggleMedication(med.id)" />
    <label :for="'med-' + med.id" style="margin-left: 0.5rem">{{ med.name }} ({{ med.time }})</label>
  </li>
</template>
