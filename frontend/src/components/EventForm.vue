<template>
  <div class="modal-overlay" role="button" tabindex="0" @click.self="close" @keydown.esc="close">
    <div class="modal">
      <h3 class="modal-title">{{ isEdit ? 'Edit Event' : 'Add Event' }}</h3>
      <form @submit.prevent="handleSubmit">
        <label class="form-field">
          Name:
          <input v-model="form.name" required />
        </label>
        <label class="form-field">
          Date & Time (IST):
          <input v-model="form.date_time" type="datetime-local" required />
          <small>Time will be saved in Indian Standard Time (IST)</small>
        </label>
        <label class="form-field">
          Description:
          <input v-model="form.description" required placeholder="Description" />
        </label>
        <label class="form-field">
          Location:
          <input v-model="form.location" required placeholder="Location / Info" />
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
});

const emit = defineEmits(['close', 'submit']);

const form = reactive({
  name: '',
  date_time: '',
  description: '',
  location: '',
});

// Function to convert UTC/ISO datetime to local datetime-local format
function convertToLocalDateTimeString(isoString) {
  if (!isoString) return '';

  try {
    const date = new Date(isoString);
    // Convert to local timezone and format for datetime-local input
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
  } catch (error) {
    console.error('Error converting datetime:', error);
    return '';
  }
}

// Function to convert local datetime-local to ISO string with proper IST offset
function convertToISOString(datetimeLocalString) {
  if (!datetimeLocalString) return '';

  try {
    // The datetime-local input is parsed by the browser in the user's local timezone.
    // Creating a Date object from it preserves this.
    const date = new Date(datetimeLocalString);
    
    // toISOString() automatically converts the date to a UTC timezone string.
    // e.g., '2025-08-13T16:35:00' (in IST) becomes '2025-08-13T11:05:00.000Z'
    const isoString = date.toISOString();

    console.log(`Converting: ${datetimeLocalString} (Local) -> ${isoString} (UTC)`);
    return isoString;
  } catch (error) {
    console.error('Error converting to ISO:', error);
    return '';
  }
}

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.name = val.name || '';
      // Convert the received datetime to local format for the input
      form.date_time = convertToLocalDateTimeString(val.date_time);
      form.description = val.description || '';
      form.location = val.location || '';
    }
  },
  { immediate: true },
);

async function handleSubmit() {
  const { event_id, service_provider_id, ...rest } = { ...props.modelValue, ...form };

  let finalDateTime;
  if (form.date_time) {
    // Convert the datetime-local value to ISO string
    finalDateTime = convertToISOString(form.date_time);
  }

  const payload = {
    ...rest,
    date_time: finalDateTime,
  };

  // Explicitly delete service_provider_id if it somehow got in
  delete payload.service_provider_id;

  console.log('Submitting event payload:', payload);
  console.log('Original datetime-local value:', form.date_time);
  console.log('Converted to ISO:', finalDateTime);

  emit('submit', payload);
  close();
}

function close() {
  emit('close');
}
</script>

<style scoped>
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
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 400px;
  color: #333;
}

.modal-title {
  color: #333;
  margin-bottom: 1rem;
  text-align: center;
}

.form-field {
  display: block;
  margin-bottom: 1rem;
  color: #333;
}

.form-field input {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: #333;
  background-color: white;
}

.form-field small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.8rem;
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
