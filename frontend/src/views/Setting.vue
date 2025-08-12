<script setup>
import { useUserStore } from '../store/userStore';
import accessibilityService from '../services/accessibilityService';
import ChangePasswordForm from '../components/ChangePasswordForm.vue';

const userStore = useUserStore();

const setFontSize = async (event) => {
  const newSize = event.target.value;
  console.log('Setting.vue: Calling updateFontSize with', newSize);
  await userStore.updateFontSize(newSize);
};

const toggleDarkMode = async () => {
  const newMode = !userStore.accessibility.darkMode;
  console.log('Setting.vue: Calling updateDarkMode with', newMode);
  await userStore.updateDarkMode(newMode);
};
</script>

<template>
  <div class="settings-container">
    <h2>Accessibility Settings</h2>

    <div class="setting-group">
      <label>Font Size:</label>
      <select :value="userStore.accessibility.fontSize" @change="setFontSize" class="styled-select">
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>
    </div>

    <div class="setting-group">
      <label>Dark Mode:</label>
      <input
        type="checkbox"
        :checked="userStore.accessibility.darkMode"
        @change="toggleDarkMode"
        class="styled-checkbox"
      />
    </div>

    <h2>Notification Preferences</h2>
    <div class="placeholder">[Notification preference will be added here]</div>

    <h2>Change Password</h2>
    <ChangePasswordForm />
  </div>
</template>

<style scoped>
.settings-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  margin-top: 20px;
  font-size: 22px;
  color: #333;
}

.setting-group {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-weight: 500;
  color: #555;
}

.styled-select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
  transition: border-color 0.2s;
  color: white;
}

.styled-select:focus {
  border-color: #3b82f6;
  outline: none;
}

.styled-checkbox {
  width: 20px;
  height: 20px;
}

.placeholder {
  padding: 10px;
  border: 1px dashed #ccc;
  border-radius: 6px;
  text-align: center;
  color: #888;
  font-size: 14px;
}
</style>
