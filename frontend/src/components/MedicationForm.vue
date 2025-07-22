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
          Time:
          <input v-model="form.time" required placeholder="e.g. 08:00 AM" />
        </label>
        <label class="form-field checkbox-field">
          Taken:
          <input v-model="form.taken" type="checkbox" />
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

const form = reactive({ name: '', time: '', taken: false });

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.name = val.name || '';
      form.time = val.time || '';
      form.taken = val.taken || false;
    }
  },
  { immediate: true },
);

function handleSubmit() {
  emit('submit', { ...props.modelValue, ...form });
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
