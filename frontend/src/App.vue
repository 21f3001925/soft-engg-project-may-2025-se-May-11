<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from './store/userStore';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

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
  <div class="app" :class="[userStore.accessibility.fontSize, userStore.accessibility.darkMode ? 'dark' : 'light']">
    <nav v-if="showNav" id="nav">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/medications" class="nav-link">Medications</router-link>
          <router-link to="/appointments" class="nav-link">Appointments</router-link>
          <router-link to="/news" class="nav-link">News</router-link>
          <router-link to="/events" class="nav-link">Events</router-link>
          <router-link to="/profile" class="nav-link">Profile</router-link>
          <router-link to="/setting" class="nav-link">Setting</router-link>
          <router-link to="/caregiver-dashboard" class="nav-link">Caregiver Dashboard</router-link>
          <router-link to="/service-provider" class="nav-link">ServiceProvider Dashboard</router-link>
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
