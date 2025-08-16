<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Menu, ChevronDown, User } from 'lucide-vue-next';
import logo from '../assets/vue.svg';
import { useUserStore } from '../store/userStore';
import { useAvatar } from '../composables/useAvatar';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const roleDropdownOpen = ref(false);

const showNav = computed(() => {
  return !['Login', 'Register'].includes(route.name);
});

const navOpen = ref(false);
const userDropdownOpen = ref(false);

const { avatarUrl: userAvatar, hasAvatar } = useAvatar();

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
};

const navLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/medications', label: 'Medications' },
  { to: '/appointments', label: 'Appointments' },
  { to: '/news', label: 'News' },
  { to: '/events', label: 'Events' },
  { to: '/profile', label: 'Profile' },
  { to: '/setting', label: 'Settings' },
  { to: '/report-analyzer', label: 'Report Analyzer' },

];

function closeDropdowns(e) {
  if (!e.target.closest('.user-dropdown') && !e.target.closest('.user-avatar')) {
    userDropdownOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', closeDropdowns);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdowns);
});
</script>

<template>
  <nav v-if="showNav" class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Left: Logo -->
        <router-link to="/dashboard" class="flex items-center gap-2">
          <img :src="logo" alt="Logo" class="h-8 w-8" />
          <span class="font-bold text-lg text-blue-700 hidden sm:inline">SeniorCare</span>
        </router-link>

        <!-- Center: Navigation Links -->
        <template v-if="userStore.isAuthenticated">
          <div class="hidden md:flex items-center space-x-8">
            <router-link
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              class="px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition"
              :class="{ 'bg-blue-100 text-blue-700': route.path === link.to }"
            >
              {{ link.label }}
            </router-link>
          </div>
        </template>

        <!-- Right: Profile and Mobile Menu -->
        <div class="flex items-center gap-2">
          <!-- Profile Section -->
          <div class="relative user-avatar">
            <button
              class="flex items-center gap-2 p-1 rounded-full hover:bg-blue-50 transition"
              @click.stop="userDropdownOpen = !userDropdownOpen"
            >
              <div class="h-8 w-8 rounded-full border border-gray-200 flex items-center justify-center bg-gray-100">
                <img v-if="hasAvatar" :src="userAvatar" alt="Avatar" class="h-8 w-8 rounded-full object-cover" />
                <User v-else :size="16" class="text-gray-500" />
              </div>
              <ChevronDown class="w-4 h-4 text-gray-500" />
            </button>
            <div
              v-if="userDropdownOpen"
              class="user-dropdown absolute right-0 mt-2 w-48 bg-white border border-gray-100 rounded-lg shadow-lg py-2 z-50"
            >
              <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-blue-50">Profile</router-link>
              <router-link to="/setting" class="block px-4 py-2 text-gray-700 hover:bg-blue-50">Settings</router-link>
              <button class="block w-full text-left px-4 py-2 text-red-600 hover:bg-red-50" @click="handleLogout">
                Logout
              </button>
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <button class="md:hidden p-2 rounded-full hover:bg-blue-50 transition ml-2" @click="navOpen = !navOpen">
            <Menu class="w-6 h-6 text-gray-700" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Menu -->
    <div v-if="showNav && navOpen" class="md:hidden bg-white border-t border-gray-100 shadow-sm">
      <div class="px-4 py-2 space-y-1">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="block px-3 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
          :class="{ 'text-blue-600 bg-blue-50': route.path === link.to }"
        >
          {{ link.label }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

button {
  cursor: pointer;
}
</style>
