<script setup>
import { useUserStore } from './store/userStore';
import TopNavBar from './components/TopNavBar.vue';
import TopNavBarProvider from './components/TopNavBarProvider.vue';
import TopNavBarCaregiver from './components/TopNavBarCaregiver.vue';
import { onMounted, computed } from 'vue';
import profileService from './services/profileService';
import { useRoute } from 'vue-router';

const userStore = useUserStore();
const route = useRoute();

// Match all caregiver dashboard and subpages
const isCaregiverDashboard = computed(() =>
  route.path === '/caregiver-dashboard' ||
  route.path.startsWith('/caregiver/seniors/')
);

const isProviderDashboard = computed(() =>
  route.path === '/service-provider'
);

onMounted(async () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const profileResponse = await profileService.getProfile();
      userStore.setUser(profileResponse.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  }
});
</script>

<template>
  <div
    :class=" [
      'app',
      userStore.accessibility.darkMode ? 'dark' : 'light',
      userStore.accessibility.fontSize,
      'flex',
      'flex-col',
      'min-h-screen',
      'bg-gray-100',
    ]"
  >
    <!-- Show TopNavBarProvider only for provider dashboard -->
    <TopNavBarProvider v-if="isProviderDashboard" />
    <!-- Show TopNavBarCaregiver for caregiver dashboard and subpages -->
    <TopNavBarCaregiver v-else-if="isCaregiverDashboard" />
    <!-- Show TopNavBar everywhere else -->
    <TopNavBar v-else />
    <main class="flex-1">
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
