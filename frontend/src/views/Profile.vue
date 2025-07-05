<script setup>
import { useUserStore } from '../store/userStore';
import catImg from '../assets/cat.png';

const userStore = useUserStore();
const user = userStore.user;
const friends = userStore.friends;
const stats = userStore.stats;

const contactEmergency = () => {
  alert(`Calling emergency number: ${userStore.user.emergencyNumber}`);
};

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    userStore.updateProfilePic(reader.result);
  };
  reader.readAsDataURL(file);
};

function emergencyContacts() {
  window.location.href = '/emergency-contacts';
}
</script>

<template>
  <div class="profile-page">
    <div class="card user-profile">
      <img class="user-avatar" :src="user.profilePic || catImg" alt="User Avatar" />
      <div class="file-upload-wrapper">
        <button class="upload-button" @click="$refs.fileInput.click()">Change Photo</button>
        <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" style="display: none" />
      </div>
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
      <h3 style="margin-top: 1px"><b>Your Contacts</b></h3>
      <hr />
      <br />
      <div>
        <div v-for="(number, name) in friends" :key="name" class="friend-item">{{ name }}</div>
      </div>

      <button class="edit-button" @click="emergencyContacts">Edit Contacts</button>
    </div>

    <div class="card user-stats">
      <h3 style="margin-top: 1px"><b>Your stats</b></h3>
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
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
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
  color: #4fc3f7;
  cursor: pointer;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
}

.user-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}

.edit-button {
  margin-top: 12px;
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: #125aa1;
}
</style>
