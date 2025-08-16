<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import profileService from '../services/profileService';
import { useUserStore } from '../store/userStore';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

onMounted(async () => {
  const token = route.query.token;
  if (token) {
    localStorage.setItem('token', token);

    try {
      const profileResponse = await profileService.getProfile();
      userStore.setUser(profileResponse.data);
    } catch (profileError) {
      console.error('Error loading user profile after OAuth login:', profileError);
    }

    router.replace('/dashboard');
  } else {
    router.replace('/login');
  }
});
</script>

<template>
  <div class="p-6 text-center text-gray-600">Signing you in...</div>
</template>
