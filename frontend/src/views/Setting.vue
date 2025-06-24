<script setup></script>
<template>
  <h1>Settings</h1>
  <div class="settings-page">
    <ul class="settings-list">
      <li>
        <RouterLink to="/settings/profile-pic">Update Profile Picture</RouterLink>
      </li>
      <li>
        <RouterLink to="/settings/change-password">Change Password</RouterLink>
      </li>
      <li>
        <RouterLink to="/settings/notifications">Notification Preferences</RouterLink>
      </li>
      <li>
        <RouterLink to="/settings/account">Account Info</RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.settings-page {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-family: sans-serif;
}

.settings-list {
  list-style: none;
  padding: 0;
}

.settings-list li {
  margin: 1rem 0;
  font-size: 1.1rem;
}

.settings-list a {
  text-decoration: none;
  color: #1480be;
  font-weight: bold;
}

.settings-list a:hover {
  text-decoration: underline;
}
h1 {
  text-align: center;
  color: #14a0f1;
}
</style>
