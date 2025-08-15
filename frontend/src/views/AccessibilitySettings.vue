<script setup>
import { useUserStore } from '../store/userStore';

const userStore = useUserStore();

const setFontSize = async (event) => {
  await userStore.updateFontSize(event.target.value);
};

const toggleDarkMode = async () => {
  await userStore.updateDarkMode(!userStore.accessibility.darkMode);
};
</script>

<template>
  <div class="accessibility-settings">
    <h2>Accessibility Settings</h2>

    <div class="setting">
      <label>Font Size:</label>
      <select :value="userStore.accessibility.fontSize" @change="setFontSize">
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>
    </div>

    <div class="setting">
      <label>Dark Mode:</label>
      <input type="checkbox" :checked="userStore.accessibility.darkMode" @change="toggleDarkMode" />
    </div>
  </div>
</template>

<style scoped>
.setting {
  margin: 10px 0;
}
</style>
