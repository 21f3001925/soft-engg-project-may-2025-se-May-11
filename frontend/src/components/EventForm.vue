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
          Date & Time:
          <input v-model="form.date_time" type="datetime-local" required />
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

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.name = val.name || '';
      // Convert ISO string to input format for datetime-local
      form.date_time = val.date_time
        ? val.date_time.slice(0, 16)
        : '';
      form.description = val.description || '';
      form.location = val.location || '';
    }
  },
  { immediate: true },
);

function handleSubmit() {
  // Ensure date_time is in ISO format
  const payload = {
    ...props.modelValue,
    ...form,
    date_time: form.date_time ? new Date(form.date_time).toISOString() : undefined,
  };
  emit('submit', payload);
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
