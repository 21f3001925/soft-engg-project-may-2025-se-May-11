<script setup></script>

<template>
  <div id="nav">
    <router-link to="/login">Login</router-link> | <router-link to="/register">Register</router-link> |
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
