<script setup>
import { onMounted } from 'vue';
import { useEmergencyStore } from '../store/emergencyStore';
import emergencyService from '../services/emergencyService';
import { Phone } from 'lucide-vue-next';

const emergencyStore = useEmergencyStore();

onMounted(() => {
  emergencyStore.fetchContactsForSenior();
});

const handleEmergencyClick = async () => {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
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
  <section
    class="mb-10 p-8 rounded-3xl shadow-xl border-0 bg-gradient-to-br from-red-500 to-red-600 text-white overflow-hidden relative"
    aria-label="Emergency contact widget"
  >
    <div class="relative z-10 text-center">
      <div class="mb-4">
        <div
          :class="[
            'w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-3',
            emergencyStore.loading ? 'animate-pulse' : '',
          ]"
        >
          <Phone class="h-8 w-8 text-white" />
        </div>
        <h3 class="text-xl font-bold mb-2">Emergency</h3>
        <p class="text-red-100 text-sm mb-4">
          {{
            emergencyStore.loading
              ? 'Loading...'
              : emergencyStore.contacts && emergencyStore.contacts.length > 0
                ? emergencyStore.contacts[0].subtitle || '24/7 support'
                : '24/7 support'
          }}
        </p>
      </div>

      <a
        v-if="emergencyStore.contacts && emergencyStore.contacts.length > 0 && emergencyStore.contacts[0].phone"
        :href="`tel:${emergencyStore.contacts[0].phone}`"
        class="w-full h-20 bg-white/20 hover:bg-white/30 text-white border-2 border-white/30 hover:border-white/50 text-lg font-semibold backdrop-blur-sm transition-all duration-300 flex items-center justify-center space-x-3 rounded-xl mb-2"
        aria-label="Call emergency contact"
      >
        <Phone class="h-6 w-6" />
        <div class="text-center">
          <div class="font-bold">{{ emergencyStore.contacts[0].name }}</div>
          <div class="text-sm opacity-90">
            {{ emergencyStore.contacts[0].relationship || emergencyStore.contacts[0].phone }}
          </div>
        </div>
      </a>

      <div v-else class="space-y-2">
        <a
          href="tel:911"
          class="w-full h-20 bg-white/20 hover:bg-white/30 text-white border-2 border-white/30 hover:border-white/50 text-lg font-semibold backdrop-blur-sm transition-all duration-300 flex items-center justify-center space-x-3 rounded-xl"
          aria-label="Call emergency services"
        >
          <Phone class="h-6 w-6" />
          <div>
            <div>CALL 108</div>
            <div class="text-sm opacity-90">Emergency Services</div>
          </div>
        </a>

        <div
          class="w-full bg-white/10 text-white border border-white/30 text-sm font-medium rounded-xl p-3 text-center"
        >
          <div class="text-yellow-200 font-semibold mb-1">⚠️ Add Your Emergency Contacts</div>
          <div class="text-xs opacity-90">Set up personal emergency contacts for faster response</div>
        </div>
      </div>

      <router-link
        to="/emergency-contacts"
        class="block mt-2 text-xs text-red-100 underline hover:text-white transition-colors"
      >
        Manage Emergency Contacts
      </router-link>

      <div v-if="emergencyStore.contacts && emergencyStore.contacts.length > 0" class="mt-3">
        <p class="text-xs text-red-100 opacity-80">Primary: {{ emergencyStore.contacts[0].name }}</p>
        <p v-if="emergencyStore.contacts.length > 1" class="text-xs text-red-100 opacity-70">
          +{{ emergencyStore.contacts.length - 1 }} more contact{{ emergencyStore.contacts.length > 2 ? 's' : '' }}
        </p>
      </div>

      <div v-else class="mt-3">
        <p class="text-xs text-red-100 opacity-80">No emergency contacts set up yet</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.w-25 {
  height: 6.25rem; /* 100px */
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
