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
</style>
