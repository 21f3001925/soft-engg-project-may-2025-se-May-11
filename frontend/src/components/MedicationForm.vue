<template>
  <div class="modal-overlay" role="button" tabindex="0" @click.self="close" @keydown.esc="close">
    <div class="modal">
      <h3 class="modal-title">{{ isEdit ? 'Edit Medication' : 'Add Medication' }}</h3>
      <form @submit.prevent="handleSubmit">
        <label class="form-field">
          Name:
          <input v-model="form.name" required />
        </label>
        <label class="form-field">
          Dosage:
          <input v-model="form.dosage" required />
        </label>
        <label class="form-field">
          Date & Time:
          <input v-model="form.time" type="datetime-local" required />
          <small>Time is saved in your local timezone.</small>
        </label>

        <label class="form-field checkbox-field" v-if="!isCaregiverView && isEdit">
          Taken:
          <input v-model="form.isTaken" type="checkbox" />
        </label>

        <div class="actions">
          <button class="submit-btn" type="submit">{{ isEdit ? 'Update' : 'Add' }}</button>
          <button class="cancel-btn" type="button" @click="close">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, defineEmits } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
  isEdit: Boolean,
  // Accept the new prop
  isCaregiverView: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'submit']);

const form = reactive({
  name: '',
  dosage: '',
  time: '',
  isTaken: false,
});

// This function now correctly converts existing times for the form input
function convertToLocalDateTimeString(isoString) {
  if (!isoString) return '';
  try {
    const date = new Date(isoString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  } catch (error) {
    return '';
  }
}

watch(
  () => props.modelValue,
  (val) => {
    if (val && Object.keys(val).length > 0) {
      form.name = val.name || '';
      form.dosage = val.dosage || '';
      form.time = convertToLocalDateTimeString(val.time);
      form.isTaken = val.isTaken || false;
    } else {
      // Reset for new medication
      form.name = '';
      form.dosage = '';
      form.time = convertToLocalDateTimeString(new Date().toISOString());
      form.isTaken = false;
    }
  },
  { immediate: true, deep: true },
);

function handleSubmit() {
  const payload = { ...form };

  // If a caregiver is submitting, delete the isTaken field from the payload
  // so the backend doesn't see it and block the request.
  if (props.isCaregiverView) {
    delete payload.isTaken;
  }

  // The parent component will handle the final conversion to ISO string
  emit('submit', payload);
  close();
}

function close() {
  emit('close');
}
</script>

<style scoped>
/* Scoped styles remain the same */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 400px;
  color: #333;
}
.modal-title {
  color: #333;
  margin-bottom: 1rem;
}
.form-field {
  display: block;
  margin-bottom: 1rem;
  color: #333;
}
.form-field small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.8rem;
}
.form-field input {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: #333;
  background-color: #fff;
}
.checkbox-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #333;
}
.actions {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}
.submit-btn {
  background-color: green;
}
.cancel-btn {
  background-color: red;
}
</style>
