<script setup>
import { onMounted } from 'vue';
import { useEmergencyContactStore } from '../store/emergencyContactStore';
import { Phone } from 'lucide-vue-next';

const contactStore = useEmergencyContactStore();

onMounted(() => {
  contactStore.fetchEmergencyContact();
});
</script>

<template>
  <div
    class="mb-10 p-8 rounded-3xl shadow-xl border-0 bg-gradient-to-br from-red-500 to-red-600 text-white overflow-hidden relative"
  >
    <div class="absolute inset-0 bg-gradient-to-r from-red-600/20 to-pink-600/20"></div>
    <div class="relative z-10 text-center">
      <div class="mb-4">
        <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-3 animate-pulse">
          <Phone class="h-8 w-8 text-white" />
        </div>
        <h3 class="text-xl font-bold mb-2">Emergency</h3>
        <p class="text-red-100 text-sm mb-4">
          {{
            contactStore.loading ? 'Loading...' : contactStore.contact ? contactStore.contact.subtitle : '24/7 support'
          }}
        </p>
      </div>
      <div v-if="contactStore.error" class="text-red-200 mb-2">{{ contactStore.error }}</div>
      <button
        v-if="contactStore.contact"
        size="lg"
        class="w-full h-25 bg-white/20 hover:bg-white/30 text-white border-2 border-white/30 hover:border-white/50 text-lg font-semibold backdrop-blur-sm transition-all duration-300 flex items-center justify-center space-x-3 rounded-xl mb-2"
      >
        <Phone class="h-6 w-6" />
        <div>
          <div>CALL NOW</div>
          <div class="text-sm opacity-90">Emergency Contact</div>
        </div>
      </button>
      <p v-if="contactStore.contact" class="text-xs text-red-100 mt-3 opacity-80">
        {{ contactStore.contact.name }} • {{ contactStore.contact.phone }}
      </p>
    </div>
  </div>
</template>
