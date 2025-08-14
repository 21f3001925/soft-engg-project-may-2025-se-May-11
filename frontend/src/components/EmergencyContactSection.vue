<script setup>
import { onMounted } from 'vue';
import { useEmergencyStore } from '../store/emergencyStore';
import emergencyService from '../services/emergencyService';
import { Phone } from 'lucide-vue-next';

const emergencyStore = useEmergencyStore();

onMounted(() => {
  emergencyStore.fetchContactsForSenior();
});

// --- THIS FUNCTION IS NOW CORRECTED ---
// It now asks for the browser's location before sending the alert.
const handleEmergencyClick = async () => {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.');
    return;
  }

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
      // Error! The user may have denied permission.
      console.error('Error getting location: ', error);
      alert('Could not get your location. A generic emergency alert will be sent.');
      // Send a generic alert without location data
      emergencyService.triggerAlert({});
    },
  );
};
</script>

<template>
  <div
    class="mb-10 p-8 rounded-3xl shadow-xl border-0 bg-gradient-to-br from-red-500 to-red-600 text-white overflow-hidden relative"
  >
    <div class="relative z-10 text-center">
      <div class="mb-4">
        <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-3">
          <Phone class="h-8 w-8 text-white" />
        </div>
        <h3 class="text-xl font-bold mb-2">Emergency</h3>
        <p class="text-red-100 text-sm mb-4">Click below to notify contacts</p>
      </div>

      <button
        @click="handleEmergencyClick"
        class="w-full h-25 bg-white/20 hover:bg-white/30 text-white border-2 border-white/30 text-lg font-semibold backdrop-blur-sm transition-all flex items-center justify-center space-x-3 rounded-xl mb-2"
      >
        <Phone class="h-6 w-6" />
        <span>CALL NOW</span>
      </button>

      <router-link to="/emergency-contacts" class="block mt-2 text-xs text-red-100 underline hover:text-white">
        Manage Emergency Contacts
      </router-link>
    </div>
  </div>
</template>
