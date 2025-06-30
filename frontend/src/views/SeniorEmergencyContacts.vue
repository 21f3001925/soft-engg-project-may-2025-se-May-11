<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useEmergencyStore } from '../store/emergencyStore';
import { useCaregiverStore } from '../store/caregiverStore';

const emergencyStore = useEmergencyStore();
const caregiverStore = useCaregiverStore();
const route = useRoute();

const seniorId = parseInt(route.params.id);

onMounted(async () => {
  await caregiverStore.fetchSeniors?.();
  await emergencyStore.fetchContactsForSenior(seniorId);
});

const contacts = computed(() => emergencyStore.contacts.filter((c) => c.seniorId === seniorId));

const seniorName = computed(() => {
  const senior = caregiverStore.assignedSeniors?.find((s) => s.id === seniorId);
  return senior ? senior.name : 'Senior';
});

function addContact() {
  console.log('Add contact button clicked');
}

function editContact(contact) {
  console.log('Edit contact button clicked');
}

function deleteContact(contactId) {
  console.log('Delete contact button clicked');
}
</script>

<template>
  <div class="container">
    <h1>{{ seniorName }}'s Emergency Contacts</h1>

    <div v-if="contacts.length === 0" class="empty">No contacts available.</div>

    <ul v-else class="contact-list">
      <li v-for="contact in contacts" :key="contact.id" class="contact-item">
        <span>{{ contact.name }} - {{ contact.phone }}</span>
        <div class="buttons">
          <button @click="editContact(contact)">Edit</button>
          <button @click="deleteContact(contact.id)">Delete</button>
        </div>
      </li>
    </ul>

    <button class="add-btn" @click="addContact">Add Emergency Contact</button>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  margin-bottom: 1rem;
}

.empty {
  font-style: italic;
  color: #666;
}

.contact-list {
  list-style: none;
  padding: 0;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0e0e0e;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  border-radius: 8px;
}

.buttons {
  display: flex;
  gap: 0.5rem;
}

button {
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.add-btn {
  margin-top: 1.5rem;
  background-color: #4caf50;
  color: white;
}
</style>
