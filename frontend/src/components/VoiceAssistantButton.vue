<template>
  <button
    @click="toggleRecording"
    :class="{
      'bg-blue-500 hover:bg-blue-600': !isRecording && !isLoading,
      'bg-red-500 animate-pulse': isRecording,
      'bg-gray-400 cursor-not-allowed': isLoading,
    }"
    class="p-3 rounded-full text-white shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-all duration-200"
    :disabled="isLoading"
  >
    <svg
      v-if="!isLoading"
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a4 4 0 01-4-4V6a4 4 0 014-4v0a4 4 0 014 4v2a4 4 0 01-4 4z"
      />
    </svg>
    <svg
      v-else
      class="animate-spin h-6 w-6 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  </button>
</template>

<script setup>
import { ref } from 'vue';
import voiceAssistantService from '../services/voiceAssistantService';

const isRecording = ref(false);
const isLoading = ref(false);
let mediaRecorder = null;
let audioChunks = [];

const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording();
  } else {
    await startRecording();
  }
};

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' }); // Use webm for broader compatibility
      sendAudioToBackend(audioBlob);
    };

    mediaRecorder.start();
    isRecording.value = true;
    console.log('Recording started.');
  } catch (err) {
    console.error('Error accessing microphone:', err);
    alert("Could not access your microphone. Please ensure it's connected and permissions are granted.");
  }
};

const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    isRecording.value = false;
    console.log('Recording stopped.');
  }
};

const sendAudioToBackend = async (audioBlob) => {
  isLoading.value = true;
  try {
    const response = await voiceAssistantService.sendVoiceQuery(audioBlob);
    const audioUrl = URL.createObjectURL(new Blob([response.data], { type: 'audio/mpeg' }));
    const audio = new Audio(audioUrl);
    audio.play();
  } catch (error) {
    console.error('Error sending audio to backend or playing response:', error);
    alert("Sorry, I couldn't process that request. Please try again.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Add any specific styles for the button here if needed */
</style>
