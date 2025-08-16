<script setup>
import { useUserStore } from '../store/userStore';
import { useEmergencyStore } from '../store/emergencyStore';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import profileService from '../services/profileService';
import emergencyService from '../services/emergencyService';
import { useAvatar } from '../composables/useAvatar';
import {
  User,
  Camera,
  Mail,
  MapPin,
  Phone,
  Flame,
  Users,
  BarChart3,
  CheckCircle,
  Pill,
  AlertTriangle,
} from 'lucide-vue-next';

const userStore = useUserStore();
const emergencyStore = useEmergencyStore();
const router = useRouter();

const user = computed(() => userStore.user);
const emergencyContacts = computed(() => emergencyStore.contacts);
const { avatarUrl: profilePicUrl, hasAvatar } = useAvatar();

const isEditing = ref(false);
const editableUser = ref({});

onMounted(async () => {
  try {
    await profileService.getProfile();
    await emergencyStore.fetchContactsForSenior();
  } catch (error) {
    console.error('Error fetching initial data:', error);
    alert('Failed to load profile data.');
  }
});

const editProfile = () => {
  editableUser.value = { ...user.value };
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
};

const saveProfile = async () => {
  try {
    const profileData = {
      username: editableUser.value.username,
      email: editableUser.value.email,
      age: editableUser.value.age ? parseInt(editableUser.value.age) : null,
      city: editableUser.value.city || null,
      country: editableUser.value.country || null,
      phone_number: editableUser.value.phone_number || null,
    };

    const response = await profileService.updateProfile(profileData);
    userStore.setUser(response.data);
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
      emergencyService.triggerAlert({});
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
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Profile</h1>
        <p class="text-gray-600">Manage your personal information and preferences</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <div class="text-center mb-6">
            <div class="relative inline-block">
              <img
                v-if="hasAvatar"
                class="w-32 h-32 rounded-full object-cover border-4 border-blue-100 shadow-lg"
                :src="profilePicUrl"
                alt="User Avatar"
              />
              <div
                v-else
                class="w-32 h-32 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center border-4 border-blue-200 shadow-lg"
              >
                <User :size="48" class="text-blue-600" />
              </div>
              <div class="absolute -bottom-2 -right-2">
                <button
                  class="bg-blue-600 text-white p-2 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
                  @click="$refs.fileInput.click()"
                  title="Change Photo"
                >
                  <Camera class="w-4 h-4" />
                </button>
              </div>
            </div>
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
          </div>

          <div v-if="user" class="space-y-4">
            <div v-if="!isEditing">
              <div class="space-y-3">
                <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                    <User class="w-4 h-4 text-blue-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-500">Name</p>
                    <p class="font-semibold text-gray-900">{{ user.username || 'Not set' }}</p>
                  </div>
                </div>

                <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                    <Mail class="w-4 h-4 text-green-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-500">Email</p>
                    <p class="font-semibold text-gray-900">{{ user.email || 'Not set' }}</p>
                  </div>
                </div>

                <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                    <User class="w-4 h-4 text-purple-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-500">Age</p>
                    <p class="font-semibold text-gray-900">{{ user.age || 'Not set' }}</p>
                  </div>
                </div>

                <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center mr-3">
                    <MapPin class="w-4 h-4 text-orange-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-500">Location</p>
                    <p class="font-semibold text-gray-900">
                      {{ user.city && user.country ? `${user.city}, ${user.country}` : 'Not set' }}
                    </p>
                  </div>
                </div>

                <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center mr-3">
                    <Phone class="w-4 h-4 text-red-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-500">Phone</p>
                    <p class="font-semibold text-gray-900">{{ user.phone_number || 'Not set' }}</p>
                  </div>
                </div>
              </div>

              <button
                class="w-full mt-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                @click="editProfile"
              >
                Edit Profile
              </button>
            </div>

            <div v-else class="space-y-4">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
                  <input
                    type="text"
                    v-model="editableUser.username"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your name"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    v-model="editableUser.email"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your email"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Age</label>
                  <input
                    type="number"
                    v-model="editableUser.age"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your age"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">City</label>
                  <input
                    type="text"
                    v-model="editableUser.city"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your city"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Country</label>
                  <input
                    type="text"
                    v-model="editableUser.country"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your country"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Phone Number</label>
                  <input
                    type="text"
                    v-model="editableUser.phone_number"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm transition-all focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 hover:border-gray-300"
                    placeholder="Enter your phone number"
                  />
                </div>
              </div>

              <div class="flex gap-3 mt-6">
                <button
                  class="flex-1 bg-gradient-to-r from-green-600 to-green-700 text-white py-3 px-4 rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  @click="saveProfile"
                >
                  Save Changes
                </button>
                <button
                  class="flex-1 bg-gradient-to-r from-gray-500 to-gray-600 text-white py-3 px-4 rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  @click="cancelEdit"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>

          <button
            class="w-full mt-6 bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 rounded-xl font-semibold hover:from-red-700 hover:to-red-800 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
            @click="contactEmergency"
          >
            <AlertTriangle class="w-5 h-5" />
            Emergency Alert
          </button>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <div class="flex items-center mb-6">
            <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center mr-3">
              <Flame class="w-5 h-5 text-red-600" />
            </div>
            <h3 class="text-xl font-bold text-gray-800">Emergency Contacts</h3>
          </div>

          <div class="space-y-4">
            <div v-if="emergencyContacts && emergencyContacts.length > 0">
              <div
                v-for="contact in emergencyContacts"
                :key="contact.contact_id"
                class="flex items-center p-3 mb-3 bg-red-50 rounded-xl border border-red-100"
              >
                <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
                  <User class="w-5 h-5 text-red-600" />
                </div>
                <div class="flex-1">
                  <p class="font-semibold text-gray-900">{{ contact.name }}</p>
                  <p class="text-sm text-gray-500">{{ contact.relationship || 'Emergency Contact' }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users class="w-8 h-8 text-gray-400" />
              </div>
              <p class="text-gray-500 text-sm">No emergency contacts added</p>
            </div>
          </div>

          <button
            class="w-full mt-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            @click="goToEmergencyContacts"
          >
            Manage Contacts
          </button>
        </div>

        <!-- Stats Card -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <div class="flex items-center mb-6">
            <div class="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center mr-3">
              <BarChart3 class="w-5 h-5 text-purple-600" />
            </div>
            <h3 class="text-xl font-bold text-gray-800">Your Statistics</h3>
          </div>

          <div class="space-y-4">
            <div class="p-4 bg-green-50 rounded-xl border border-green-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                    <CheckCircle class="w-4 h-4 text-green-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Appointments</p>
                    <p class="font-bold text-gray-900">Missed: {{ user?.appointments_missed || 0 }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-4 bg-orange-50 rounded-xl border border-orange-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center mr-3">
                    <Pill class="w-4 h-4 text-orange-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Medications</p>
                    <p class="font-bold text-gray-900">Missed: {{ user?.medications_missed || 0 }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
