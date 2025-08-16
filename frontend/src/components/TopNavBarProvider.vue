<script setup>
import { useRouter } from 'vue-router';
import logo from '../assets/vue.svg';

const router = useRouter();

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};
</script>

<template>
  <nav class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
      <router-link to="/service-provider" class="flex items-center gap-2">
        <img :src="logo" alt="Logo" class="h-8 w-8" />
        <span class="font-bold text-lg text-blue-700 hidden sm:inline">SeniorCare</span>
      </router-link>
      <button
        class="px-4 py-2 rounded-lg font-medium text-red-600 bg-white border border-gray-300 hover:bg-red-50 transition"
        @click="handleLogout"
      >
        Logout
      </button>
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
