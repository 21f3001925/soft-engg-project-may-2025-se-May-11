<script setup>
import { useUserStore } from '../store/userStore';
import catImg from '../assets/cat.png';
import { ref, onMounted } from 'vue';
import profileService from '../services/profileService';

const userStore = useUserStore();
const user = ref(userStore.user);
const friends = userStore.friends;
const stats = userStore.stats;

onMounted(async () => {
  try {
    const response = await profileService.getProfile();
    userStore.setUser(response.data);
    user.value = response.data;
  } catch (error) {
    console.error('Error fetching profile:', error);
    alert('Failed to load profile data. Please try again later.');
  }
});

const isEditing = ref(false);
const originalUser = ref({});

const editProfile = () => {
  originalUser.value = { ...user.value }; // Store a copy of the original user data
  isEditing.value = true;
};

const cancelEdit = () => {
  user.value = { ...originalUser.value }; // Revert changes
  isEditing.value = false;
};

const saveProfile = async () => {
  try {
    // Exclude avatar_url from the data sent for profile update
    const { avatar_url, ...profileData } = user.value;
    const response = await profileService.updateProfile(profileData);
    userStore.setUser(response.data);
    user.value = response.data;
    isEditing.value = false;
    alert('Profile updated successfully!');
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Failed to update profile. Please try again later.');
  }
};

const contactEmergency = () => {
  alert(`Calling emergency number: ${userStore.user.emergencyNumber}`);
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const response = await profileService.uploadAvatar(file);
    userStore.setUser(response.data);
    user.value = response.data;
    alert('Avatar uploaded successfully!');
  } catch (error) {
    console.error('Error uploading avatar:', error);
    alert('Failed to upload avatar. Please try again later.');
  }
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
        <div v-if="!isEditing">
          <p><strong>Name:</strong> {{ user.username }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>
          <p><strong>City:</strong> {{ user.city }}</p>
          <p><strong>Country:</strong> {{ user.country }}</p>
          <p><strong>Emergency Number:</strong> {{ user.emergencyNumber }}</p>
          <p v-if="user.news_categories"><strong>News Categories:</strong> {{ user.news_categories }}</p>
          <button class="edit-button" @click="editProfile">Edit Profile</button>
        </div>
        <div v-else>
          <p><strong>Name:</strong> <input type="text" v-model="user.username" /></p>
          <p><strong>Email:</strong> <input type="email" v-model="user.email" /></p>
          <p><strong>Age:</strong> <input type="number" v-model="user.age" /></p>
          <p><strong>City:</strong> <input type="text" v-model="user.city" /></p>
          <p><strong>Country:</strong> <input type="text" v-model="user.country" /></p>
          <p><strong>Emergency Number:</strong> <input type="text" v-model="user.emergencyNumber" /></p>
          <p v-if="user.news_categories">
            <strong>News Categories:</strong> <input type="text" v-model="user.news_categories" />
          </p>
          <button class="edit-button" @click="saveProfile">Save Profile</button>
          <button class="edit-button" @click="cancelEdit">Cancel</button>
        </div>
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
        <li>Topics Liked: {{ user.topics_liked }}</li>
        <li>Comments Posted: {{ user.comments_posted }}</li>
        <li>Appointments Missed: {{ user.appointments_missed }}</li>
        <li>Medications Missed: {{ user.medications_missed }}</li>
        <li>Total Screentime (Hrs): {{ user.total_screentime }}</li>
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
