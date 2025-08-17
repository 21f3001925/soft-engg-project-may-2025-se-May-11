<template>
  <div class="chatbot-container border rounded-lg p-4 mt-6">
    <h3 class="text-xl font-semibold mb-4">Chat with Caregiver AI</h3>
    <div class="message-window h-64 overflow-y-auto mb-4 p-2 border rounded-md bg-gray-50">
      <div v-for="(msg, index) in messages" :key="index" :class="`chat-message ${msg.sender}`">
        <p class="font-bold">{{ msg.sender === 'user' ? 'You' : 'AI' }}</p>
        <p>{{ msg.text }}</p>
      </div>
      <div v-if="loading" class="chat-message ai">
        <p>AI is typing...</p>
      </div>
    </div>
    <div class="flex space-x-2">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Ask a question about the senior..."
        class="flex-grow border rounded-md p-2"
      />
      <button @click="sendMessage" :disabled="!newMessage || loading" class="btn-primary">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import caregiverChatService from '../services/caregiverChatService';

const props = defineProps({
  seniorId: {
    type: String,
    required: true,
  },
});

const messages = ref([]);
const newMessage = ref('');
const loading = ref(false);

const sendMessage = async () => {
  if (!newMessage.value) return;

  const userMessage = newMessage.value;
  messages.value.push({ sender: 'user', text: userMessage });
  newMessage.value = '';
  loading.value = true;

  try {
    const response = await caregiverChatService.sendMessage(props.seniorId, userMessage);
    messages.value.push({ sender: 'ai', text: response.data.response });
  } catch (error) {
    messages.value.push({ sender: 'ai', text: 'Sorry, I encountered an error. Please try again.' });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.chat-message {
  @apply p-2 mb-2 rounded-lg;
}
.user {
  @apply bg-blue-100 text-right;
}
.ai {
  @apply bg-gray-200;
}
</style>
