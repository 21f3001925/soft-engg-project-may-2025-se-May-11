<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useEmergencyStore } from '../store/emergencyStore';
import { useCaregiverStore } from '../store/caregiverStore';
import EmergencyContactForm from '../components/EmergencyContactForm.vue';

const emergencyStore = useEmergencyStore();
const caregiverStore = useCaregiverStore();
const route = useRoute();

const seniorId = parseInt(route.params.id);
const selectedContact = ref(null);
const showModal = ref(false);
const isEdit = ref(false);
const toastMessage = ref('');

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
  selectedContact.value = null;
  isEdit.value = false;
  showModal.value = true;
}

function editContact(contact) {
  selectedContact.value = { ...contact };
  isEdit.value = true;
  showModal.value = true;
}

function deleteContact(contactId) {
  emergencyStore.contacts = emergencyStore.contacts.filter((c) => c.id !== contactId);
  showToast('Contact deleted');
}

function handleSubmit(newContact) {
  if (isEdit.value) {
    const index = emergencyStore.contacts.findIndex((c) => c.id === newContact.id);
    if (index !== -1) {
      emergencyStore.contacts[index] = { ...newContact };
      showToast('Contact updated');
    }
  } else {
    emergencyStore.contacts.push({
      ...newContact,
      id: Date.now(),
      seniorId,
    });
    showToast('Contact added');
  }
  showModal.value = false;
}

function showToast(msg) {
  toastMessage.value = msg;
  setTimeout(() => (toastMessage.value = ''), 2000);
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
          <button class="edit-btn" @click="editContact(contact)">Edit</button>
          <button class="delete-btn" @click="deleteContact(contact.id)">Delete</button>
        </div>
      </li>
    </ul>

    <button class="add-btn" @click="addContact">Add Emergency Contact</button>

    <EmergencyContactForm
      v-if="showModal"
      :model-value="selectedContact"
      :is-edit="isEdit"
      @submit="handleSubmit"
      @close="showModal = false"
    />

    <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
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
  color: #1480be;
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
  background-color: #f9f9f9;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  border-radius: 8px;
  color: black;
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

.edit-btn {
  background-color: blue;
}

.delete-btn {
  background-color: red;
}
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #4caf50;
  color: white;
  padding: 12px 20px;
  border-radius: 5px;
  z-index: 9999;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  animation:
    fadein 0.3s ease,
    fadeout 0.3s ease 1.7s;
}

@keyframes fadein {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

@keyframes fadeout {
  from {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
}
</style>
