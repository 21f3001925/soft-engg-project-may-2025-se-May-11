<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Menu, Bell, User, ChevronDown } from 'lucide-vue-next';
import logo from './assets/vue.svg';
import avatar from './assets/cat.png';

const router = useRouter();
const route = useRoute();

const showNav = computed(() => {
  return !['Login', 'Register'].includes(route.name);
});

const navOpen = ref(false);
const userDropdownOpen = ref(false);
const notifications = ref([
  { id: 1, text: 'Appointment at 11:30 AM' },
  { id: 2, text: 'New message from Social Hub' },
]);

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};

const navLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/medications', label: 'Medications' },
  { to: '/appointments', label: 'Appointments' },
  { to: '/news', label: 'News' },
  { to: '/events', label: 'Events' },
  { to: '/profile', label: 'Profile' },
  { to: '/setting', label: 'Setting' },
];
</script>

<template>
  <div class="app min-h-screen bg-gray-50">
    <nav v-if="showNav" class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-3">
            <router-link to="/dashboard" class="flex items-center gap-2">
              <img :src="logo" alt="Logo" class="h-8 w-8" />
              <span class="font-bold text-lg text-blue-700 hidden sm:inline">SeniorCare</span>
            </router-link>
          </div>
          <div class="hidden md:flex gap-2 lg:gap-4">
            <router-link
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              class="px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition"
              active-class="bg-blue-100 text-blue-700"
              exact-active-class="bg-blue-100 text-blue-700"
            >
              {{ link.label }}
            </router-link>
          </div>
          <div class="flex items-center gap-2">
            <div class="relative">
              <button class="p-2 rounded-full hover:bg-blue-50 transition" @click="userDropdownOpen = false">
                <Bell class="w-5 h-5 text-gray-500" />
                <span
                  v-if="notifications.length"
                  class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5"
                  >{{ notifications.length }}</span
                >
              </button>
            </div>
            <div class="relative">
              <button
                class="flex items-center gap-2 p-1 rounded-full hover:bg-blue-50 transition"
                @click="userDropdownOpen = !userDropdownOpen"
              >
                <img :src="avatar" alt="Avatar" class="h-8 w-8 rounded-full border border-gray-200" />
                <ChevronDown class="w-4 h-4 text-gray-500" />
              </button>
              <div
                v-if="userDropdownOpen"
                class="absolute right-0 mt-2 w-48 bg-white border border-gray-100 rounded-lg shadow-lg py-2 z-50"
              >
                <router-link to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-blue-50">Profile</router-link>
                <router-link to="/setting" class="block px-4 py-2 text-gray-700 hover:bg-blue-50">Settings</router-link>
                <button class="block w-full text-left px-4 py-2 text-red-600 hover:bg-red-50" @click="handleLogout">
                  Logout
                </button>
              </div>
            </div>
            <button class="md:hidden p-2 rounded-full hover:bg-blue-50 transition ml-2" @click="navOpen = !navOpen">
              <Menu class="w-6 h-6 text-gray-700" />
            </button>
          </div>
        </div>
      </div>
      <div v-if="navOpen" class="md:hidden bg-white border-t border-gray-100 shadow-sm">
        <div class="flex flex-col gap-1 px-4 py-2">
          <router-link
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition"
            active-class="bg-blue-100 text-blue-700"
            exact-active-class="bg-blue-100 text-blue-700"
            @click="navOpen = false"
          >
            {{ link.label }}
          </router-link>
        </div>
      </div>
    </nav>
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
