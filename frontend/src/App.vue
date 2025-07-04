<script setup>
import TopNavBar from './components/TopNavBar.vue';
</script>

<template>
  <div class="app min-h-screen bg-gray-50">
    <TopNavBar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: #f9fafb;
}

/* Font Size Classes */
.small {
  font-size: 16px;
}
.medium {
  font-size: 19px;
}
.large {
  font-size: 25px;
}

/* Theme Classes */
.light {
  background-color: white;
  color: black;
}

.dark {
  background-color: #121212;
  color: #f0f0f0;
}

.dark a {
  color: #90caf9;
}

.light a {
  color: #1976d2;
}

.nav-content {
  background-color: inherit;
  color: inherit;
}

.logout-button {
  background-color: transparent;
  color: inherit;
  border: 1px solid currentColor;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
