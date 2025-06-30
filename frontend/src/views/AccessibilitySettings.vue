<script setup>
import { useUserStore } from '../store/userStore';

const userStore = useUserStore();

const setFontSize = (size) => {
  userStore.accessibility.fontSize = size;
};

const toggleDarkMode = () => {
  userStore.accessibility.darkMode = !userStore.accessibility.darkMode;
};
</script>

<template>
  <div class="accessibility-settings">
    <h2>Accessibility Settings</h2>

    <div class="setting">
      <label>Font Size:</label>
      <select v-model="userStore.accessibility.fontSize">
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
