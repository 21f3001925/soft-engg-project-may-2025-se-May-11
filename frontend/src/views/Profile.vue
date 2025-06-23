<script setup>
import { useUserStore } from '../store/userStore';

const userStore = useUserStore();

const user = userStore.user;
const friends = userStore.friends;
const stats = userStore.stats;

const contactEmergency = () => {
  alert(`Calling emergency number: ${userStore.user.emergencyNumber}`);
};
</script>

<template>
  <div class="profile-page">
    <div class="card user-profile">
      <img
        class="user-avatar"
        src="/home/rishit/soft-engg-project-may-2025-se-May-11/frontend/src/assets/cat.png"
        alt="User Avatar"
      />
      <div class="user-info">
        <p><strong>Name:</strong> {{ user.username }}</p>
        <p><strong>Age:</strong> {{ user.age }}</p>
        <p><strong>City:</strong> {{ user.city }}</p>
        <p><strong>Country:</strong> {{ user.country }}</p>
        <p><strong>Emergency Number:</strong> {{ user.emergencyNumber }}</p>
      </div>
      <button class="emergency-button" @click="contactEmergency">Contact Emergency Number</button>
    </div>

    <div class="card friends-list">
      <h3 style="margin-top: 1px">Your Friends</h3>
      <hr />
      <br />
      <div>
        <div v-for="friend in friends" :key="friend.id" class="friend-item">{{ friend }}</div>
      </div>
    </div>

    <div class="card user-stats">
      <h3 style="margin-top: 1px">Your stats</h3>
      <hr />
      <br />
      <ul>
        <li>Topics Liked: {{ stats.topicsLiked }}</li>
        <li>Comments Posted: {{ stats.commentsPosted }}</li>
        <li>Appointments Missed: {{ stats.appointmentsMissed }}</li>
        <li>Medications Missed: {{ stats.medicationsMissed }}</li>
        <li>Total Screentime (Hrs): {{ stats.totalScreentime }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  margin-left: 200px;
  display: flex;
  flex-wrap: wrap;
  text-align: center;
  gap: 20px;
  padding: 20px;
}

.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  width: 300px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 12px;
}

.emergency-button {
  background-color: red;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 12px;
}

.friend-list ul,
.user-stats ul {
  list-style: none;
  align-items: center;
  text-align: center;
  padding: 0px;
  margin: 0px;
}

.friend-list li,
.user-stats li {
  margin-bottom: 8px;
  align-items: center;
  text-align: center;
}

.friend-item:hover {
  color: #4fc3f7; /* Light blue on hover */
  cursor: pointer; /* Optional if you want it to feel interactive */
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
}
</style>
