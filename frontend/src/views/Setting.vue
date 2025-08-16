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
</script>

<template>
  <div class="settings-container">
    <h2 class="section-heading">Accessibility Settings</h2>

    <div class="setting-group">
      <label>Text Size:</label>
      <select :value="userStore.accessibility.fontSize" @change="setFontSize" class="styled-select">
        <option value="small">Small - Easy to read</option>
        <option value="medium">Medium - Standard size</option>
        <option value="large">Large - Enhanced visibility</option>
      </select>
    </div>

    <div class="setting-group">
      <label>Theme:</label>
      <div class="theme-options">
        <label class="theme-option" :class="{ selected: !userStore.accessibility.darkMode }">
          <input
            type="radio"
            name="theme"
            :checked="!userStore.accessibility.darkMode"
            @change="() => userStore.updateDarkMode(false)"
            class="theme-radio"
          />
          <span class="theme-label">
            <span class="theme-icon">☀️</span>
            Light Theme
          </span>
        </label>
        <label class="theme-option" :class="{ selected: userStore.accessibility.darkMode }">
          <input
            type="radio"
            name="theme"
            :checked="userStore.accessibility.darkMode"
            @change="() => userStore.updateDarkMode(true)"
            class="theme-radio"
          />
          <span class="theme-label">
            <span class="theme-icon">🌙</span>
            Dark Theme
          </span>
        </label>
      </div>
    </div>

    <h2 class="section-heading">Change Password</h2>
    <ChangePasswordForm />
  </div>
</template>

<style scoped>
.settings-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  transition: all 0.3s ease;
}

h2,
.section-heading {
  margin-top: 20px;
  font-size: 22px;
  color: #333;
  font-weight: 600;
  margin-bottom: 15px;
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
  color: #333;
  background-color: white;
  cursor: pointer;
}

.styled-select:focus {
  border-color: #3b82f6;
  outline: none;
}

.theme-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: white;
}

.theme-option:hover {
  border-color: #3b82f6;
  background-color: #f8fafc;
}

.theme-radio {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #3b82f6;
  margin: 0;
}

.theme-label {
  color: #555;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  flex: 1;
}

.theme-icon {
  font-size: 18px;
}

/* Radio button styling */
.theme-option input[type='radio']:checked {
  accent-color: #3b82f6;
}

/* Selected theme option styling */
.theme-option.selected {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.theme-option.selected .theme-label {
  color: #3b82f6;
  font-weight: 600;
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
