<!-- <script setup></script>
<template>
  <div class="accessibility-settings">
    <h2>Accessibility Settings</h2>

    <div class="setting">
      <label>Font Size: </label>
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
  <br />
  <div class="notification-preference">
    <h2>Notification Preferences</h2>
  </div>
  <br />
  <div class="change-password">
    <h2>Change Password</h2>
  </div>
</template>

<style scoped>
.settings-page {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-family: sans-serif;
}

.settings-list {
  list-style: none;
  padding: 0;
}

.settings-list li {
  margin: 1rem 0;
  font-size: 1.1rem;
}

.settings-list a {
  text-decoration: none;
  color: #1480be;
  font-weight: bold;
}

.settings-list a:hover {
  text-decoration: underline;
}
h1 {
  text-align: center;
  color: #14a0f1;
}
</style> -->

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
      <label>Font Size: </label>
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
  <br />
  <div class="notification-preference">
    <h2>Notification Preferences</h2>
  </div>
  <br />
  <div class="change-password">
    <h2>Change Password</h2>
  </div>
</template>

<style scoped>
.setting {
  margin: 10px 0;
}
</style>
