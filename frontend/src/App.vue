<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const showNav = computed(() => {
  return !['Login', 'Register'].includes(route.name);
});
</script>

<template>
  <div v-if="showNav" id="nav">
    <router-link to="/">Home</router-link>
  </div>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
#nav {
  padding: 30px;
  text-align: center;
}
#nav a {
  font-weight: bold;
  color: #2c4e50;
  margin: 0 10px;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
main {
  padding: 1rem;
}
</style>
