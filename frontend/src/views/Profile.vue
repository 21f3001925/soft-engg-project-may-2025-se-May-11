<script setup>
import { useUserStore } from '../store/userStore';
import { useEmergencyStore } from '../store/emergencyStore';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import profileService from '../services/profileService';
import emergencyService from '../services/emergencyService';
import { useAvatar } from '../composables/useAvatar';

const userStore = useUserStore();
const emergencyStore = useEmergencyStore();
const router = useRouter();

// --- For displaying data (read-only) ---
const user = computed(() => userStore.user);
const emergencyContacts = computed(() => emergencyStore.contacts);
const { avatarUrl: profilePicUrl } = useAvatar();

// --- For editing data in the form (writable) ---
const isEditing = ref(false);
const editableUser = ref({}); // This will hold the data for the edit form

onMounted(async () => {
  try {
    await profileService.getProfile(); // The store will be updated internally
    await emergencyStore.fetchContactsForSenior();
  } catch (error) {
    console.error('Error fetching initial data:', error);
    alert('Failed to load profile data.');
  }
});

const editProfile = () => {
  // Copy the current user data into our editable object
  editableUser.value = { ...user.value };
  isEditing.value = true;
};

const cancelEdit = () => {
  // Just hide the form; no data needs to be reverted
  isEditing.value = false;
};

const saveProfile = async () => {
  try {
    // Use the data from our editable object to send the update
    const { avatar_url, ...profileData } = editableUser.value;
    const response = await profileService.updateProfile(profileData);
    userStore.setUser(response.data); // Update the store with the new data
    isEditing.value = false;
    alert('Profile updated successfully!');
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Failed to update profile.');
  }
};

const contactEmergency = async () => {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.');
    return;
  }

  // Ask the browser for the user's current position
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      // Success! We have the location.
      const location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      };

      try {
        await emergencyService.triggerAlert(location);
        alert('Success! Your location has been sent to your caregiver and emergency contacts.');
      } catch (error) {
        console.error('Error triggering emergency alert:', error);
        alert('Failed to send alert. Please try again.');
      }
    },
    (error) => {
      // Error! The user may have denied permission or there was another issue.
      console.error('Error getting location: ', error);
      alert('Could not get your location. A generic emergency alert will be sent.');
      // Optional: still send an alert without location
      // emergencyService.triggerAlert({});
    },
  );
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const response = await profileService.uploadAvatar(file);
    userStore.setUser(response.data);
    alert('Avatar uploaded successfully!');
  } catch (error) {
    console.error('Error uploading avatar:', error);
    alert('Failed to upload avatar. Please try again later.');
  }
};

function goToEmergencyContacts() {
  router.push('/emergency-contacts');
}
</script>

<template>
  <div class="profile-page">
    <div class="card user-profile">
      <img class="user-avatar" :src="profilePicUrl" alt="User Avatar" />
      <div class="file-upload-wrapper">
        <button class="upload-button" @click="$refs.fileInput.click()">Change Photo</button>
        <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="onFileChange" />
      </div>
      <div class="user-info">
        <div v-if="!isEditing">
          <p><strong>Name:</strong> {{ user.username }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>
          <p><strong>City:</strong> {{ user.city }}</p>
          <p><strong>Country:</strong> {{ user.country }}</p>
          <p><strong>Phone Number:</strong> {{ user.phone_number }}</p>
          <p v-if="user.news_categories"><strong>News Categories:</strong> {{ user.news_categories }}</p>
          <button class="edit-button" @click="editProfile">Edit Profile</button>
        </div>
        <div v-else>
          <p><strong>Name:</strong> <input type="text" v-model="editableUser.username" /></p>
          <p><strong>Email:</strong> <input type="email" v-model="editableUser.email" /></p>
          <p><strong>Age:</strong> <input type="number" v-model="editableUser.age" /></p>
          <p><strong>City:</strong> <input type="text" v-model="editableUser.city" /></p>
          <p><strong>Country:</strong> <input type="text" v-model="editableUser.country" /></p>
          <p><strong>Phone Number:</strong> <input type="text" v-model="editableUser.phone_number" /></p>
          <p v-if="editableUser.news_categories">
            <strong>News Categories:</strong> <input type="text" v-model="editableUser.news_categories" />
          </p>
          <button class="edit-button" @click="saveProfile">Save Profile</button>
          <button class="edit-button" @click="cancelEdit">Cancel</button>
        </div>
      </div>
      <button class="emergency-button" @click="contactEmergency">Notify Emergency Contacts</button>
    </div>

    <div class="card friends-list">
      <h3 style="margin-top: 1px"><b>Your Emergency Contacts</b></h3>
      <hr />
      <br />
      <div>
        <div v-for="contact in emergencyContacts" :key="contact.contact_id" class="friend-item">{{ contact.name }}</div>
      </div>
      <button class="edit-button" @click="goToEmergencyContacts">Edit Contacts</button>
    </div>

    <div class="card user-stats">
      <h3 style="margin-top: 1px"><b>Your stats</b></h3>
      <hr />
      <br />
      <ul>
        <li>Topics Liked: {{ user?.topics_liked }}</li>
        <li>Comments Posted: {{ user?.comments_posted }}</li>
        <li>Appointments Missed: {{ user?.appointments_missed }}</li>
        <li>Medications Missed: {{ user?.medications_missed }}</li>
        <li>Total Screentime (Hrs): {{ user?.total_screentime }}</li>
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
.emergency-button {
  background-color: red;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 12px;
}
.friend-item:hover {
  color: #4fc3f7;
  cursor: pointer;
}
.user-info p {
  text-align: left;
}
.user-info input {
  width: 100%;
}
</style>
