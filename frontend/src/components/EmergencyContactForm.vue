<template>
  <div class="modal-overlay" role="button" tabindex="0" @click.self="close" @keydown.esc="close">
    <div class="modal">
      <h3 class="modal-title">{{ isEdit ? 'Edit Contact' : 'Add Contact' }}</h3>
      <form @submit.prevent="handleSubmit">
        <label class="form-field">
          Name:
          <input v-model="form.name" required />
        </label>
        <label class="form-field">
          Phone:
          <input v-model="form.phone" required />
        </label>
        <div class="actions">
          <button type="submit">{{ isEdit ? 'Update' : 'Add' }}</button>
          <button type="button" @click="close">Cancel</button>
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

const form = reactive({ name: '', phone: '' });

watch(
  () => props.modelValue,
  (val) => {
    form.name = val?.name || '';
    form.phone = val?.phone || '';
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
  color: black;
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

input {
  width: 100%;
  margin-top: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.actions {
  display: flex;
  justify-content: space-between;
}
</style>
