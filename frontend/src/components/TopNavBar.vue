<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Menu, Bell, ChevronDown, X } from 'lucide-vue-next';
import logo from '../assets/vue.svg';
import avatar from '../assets/cat.png';
import { useNotificationStore } from '../store/notificationStore';

const router = useRouter();
const route = useRoute();
const notificationStore = useNotificationStore();

const showNav = computed(() => {
  return !['Login', 'Register'].includes(route.name);
});

const navOpen = ref(false);
const userDropdownOpen = ref(false);
const notificationDropdownOpen = ref(false);

const notifications = computed(() => notificationStore.notifications);

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

function openNotifications() {
  notificationDropdownOpen.value = !notificationDropdownOpen.value;
}

function markAllAsRead() {
  notificationStore.markAllAsRead();
}

function dismissNotification(id) {
  notificationStore.dismissNotification(id);
}

function closeDropdowns(e) {
  if (!e.target.closest('.notification-dropdown') && !e.target.closest('.notification-bell')) {
    notificationDropdownOpen.value = false;
  }
  if (!e.target.closest('.user-dropdown') && !e.target.closest('.user-avatar')) {
    userDropdownOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', closeDropdowns);
  notificationStore.fetchNotifications();
});
onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdowns);
});
</script>

<template>
  <nav class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex items-center gap-3">
          <router-link :to="showNav ? '/dashboard' : '/'" class="flex items-center gap-2">
            <img :src="logo" alt="Logo" class="h-8 w-8" />
            <span class="font-bold text-lg text-blue-700 hidden sm:inline">SeniorCare</span>
          </router-link>
        </div>
        <template v-if="showNav">
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
            <div class="relative notification-bell">
              <button class="p-2 rounded-full hover:bg-blue-50 transition relative" @click.stop="openNotifications">
                <Bell class="w-5 h-5 text-gray-500" />
                <span
                  v-if="notifications.length"
                  class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5"
                  >{{ notifications.length }}</span
                >
              </button>
              <div
                v-if="notificationDropdownOpen"
                class="notification-dropdown absolute right-0 mt-2 w-72 bg-white border border-gray-100 rounded-lg shadow-lg py-2 z-50"
              >
                <div class="flex items-center justify-between px-4 pb-2">
                  <span class="font-semibold text-gray-700 text-base">Notifications</span>
                  <button
                    v-if="notifications.length"
                    class="text-xs text-blue-600 hover:underline"
                    @click="markAllAsRead"
                  >
                    Mark all as read
                  </button>
                </div>
                <div v-if="notifications.length === 0" class="px-4 py-3 text-gray-400 text-sm text-center">
                  No new notifications
                </div>
                <div v-else class="divide-y divide-gray-100">
                  <div
                    v-for="n in notifications"
                    :key="n.id"
                    class="flex items-center justify-between px-4 py-2 hover:bg-blue-50 text-sm group"
                  >
                    <span class="text-gray-700">{{ n.text }}</span>
                    <button class="ml-2 p-1 rounded-full hover:bg-red-100" @click="dismissNotification(n.id)">
                      <X class="w-4 h-4 text-red-400 group-hover:text-red-600" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="relative user-avatar">
              <button
                class="flex items-center gap-2 p-1 rounded-full hover:bg-blue-50 transition"
                @click.stop="userDropdownOpen = !userDropdownOpen"
              >
                <img :src="avatar" alt="Avatar" class="h-8 w-8 rounded-full border border-gray-200" />
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
            <button class="md:hidden p-2 rounded-full hover:bg-blue-50 transition ml-2" @click="navOpen = !navOpen">
              <Menu class="w-6 h-6 text-gray-700" />
            </button>
          </div>
        </template>
      </div>
    </div>
    <div v-if="showNav && navOpen" class="md:hidden bg-white border-t border-gray-100 shadow-sm">
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
</template>

<style scoped></style>
