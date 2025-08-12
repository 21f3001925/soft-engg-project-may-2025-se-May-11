<script setup>
import { ref } from 'vue';
import authService from '../services/authService';

const currentPassword = ref('');
const newPassword = ref('');
const confirmNewPassword = ref('');
const message = ref('');
const error = ref('');
const loading = ref(false);

const handleChangePassword = async () => {
  message.value = '';
  error.value = '';
  if (newPassword.value !== confirmNewPassword.value) {
    error.value = 'New password and confirmation do not match.';
    return;
  }

  loading.value = true;
  try {
    await authService.changePassword(currentPassword.value, newPassword.value);
    message.value = 'Password changed successfully!';
    currentPassword.value = '';
    newPassword.value = '';
    confirmNewPassword.value = '';
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to change password.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="change-password-form">
    <form @submit.prevent="handleChangePassword" class="space-y-4">
      <div>
        <label for="current-password" class="block text-sm font-medium text-gray-700">Current Password</label>
        <input
          id="current-password"
          v-model="currentPassword"
          type="password"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label for="new-password" class="block text-sm font-medium text-gray-700">New Password</label>
        <input
          id="new-password"
          v-model="newPassword"
          type="password"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label for="confirm-new-password" class="block text-sm font-medium text-gray-700">Confirm New Password</label>
        <input
          id="confirm-new-password"
          v-model="confirmNewPassword"
          type="password"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Changing...' : 'Change Password' }}
      </button>
    </form>
    <p v-if="message" class="mt-3 text-sm text-green-600">{{ message }}</p>
    <p v-if="error" class="mt-3 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<style scoped></style>
