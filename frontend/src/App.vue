<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const showNav = computed(() => {
  return !['Login', 'Register'].includes(route.name);
});

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};
</script>

<template>
  <div class="app">
    <nav v-if="showNav" id="nav">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/news" class="nav-link">News</router-link>
          <router-link to="/events" class="nav-link">Events</router-link>
          <router-link to="/medications" class="nav-link">Medications</router-link>
        </div>
        <div class="nav-right">
          <button class="logout-button" @click="handleLogout">Logout</button>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
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

.nav-right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.logout-button {
  display: flex;
  background-color: #dc3545;
  border: none;
  color: #eeeeee;
  font-weight: bold;
  cursor: pointer;
}

main {
  padding: 1rem;
}
</style>
