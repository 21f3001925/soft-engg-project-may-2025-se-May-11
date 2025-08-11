<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

onMounted(() => {
  const token = route.query.token;
  if (token) {
    localStorage.setItem('token', token);
    router.replace('/dashboard');
  } else {
    router.replace('/login');
  }
});
</script>

<template>
  <div class="p-6 text-center text-gray-600">Signing you in...</div>
</template>
