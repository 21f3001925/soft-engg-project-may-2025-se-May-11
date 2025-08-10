<script setup>
import { ref, onMounted } from 'vue';
import { useEmergencyStore } from '../store/emergencyStore';
import EmergencyContactForm from '../components/EmergencyContactForm.vue';

const emergencyStore = useEmergencyStore();

const showModal = ref(false);
const isEdit = ref(false);
const selectedContact = ref(null);
const editId = ref(null);
const toastMessage = ref('');

onMounted(() => {
  emergencyStore.fetchContactsForSenior();
});

function addContact() {
  selectedContact.value = { name: '', relation: '', phone: '' };
  isEdit.value = false;
  showModal.value = true;
}

function editContact(contact) {
  selectedContact.value = { ...contact };
  isEdit.value = true;
  editId.value = contact.contact_id;
  showModal.value = true;
}

async function deleteContact(contact) {
  await emergencyStore.deleteContact(contact.contact_id);
  showToast('Contact deleted');
}

async function handleFormSubmit(contactData) {
  console.log('Submitting contact:', contactData);
  if (isEdit.value) {
    await emergencyStore.updateContact({ ...contactData, contact_id: editId.value });
    showToast('Contact updated');
  } else {
    await emergencyStore.addContact(contactData);
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
    <h1>Edit Your Contacts</h1>
    <br />

    <div v-if="emergencyStore.contacts.length === 0" class="empty">No contacts added yet.</div>

    <ul v-else class="contact-list">
      <li v-for="contact in emergencyStore.contacts" :key="contact.contact_id" class="contact-item">
        <span>{{ contact.name }} ({{ contact.relation }}) - {{ contact.phone }}</span>
        <div class="buttons">
          <button class="edit-button" @click="editContact(contact)">Edit</button>
          <button class="delete-button" @click="deleteContact(contact)">Delete</button>
        </div>
      </li>
    </ul>

    <button class="add-btn" @click="addContact">Add Contact</button>

    <EmergencyContactForm
      v-if="showModal"
      :model-value="selectedContact"
      :is-edit="isEdit"
      @submit="handleFormSubmit"
      @close="showModal = false"
    />

    <div v-if="toastMessage" class="toast">{{ toastMessage }}</div>
  </div>
</template>

<style scoped>
.container {
  max-width: 500px;
  margin: 30px auto;
  text-align: center;
}

h1 {
  margin-bottom: 1rem;
  color: #1480be;
  font-size: 30px;
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
  margin-top: 1rem;
  background-color: #4caf50;
  color: white;
}

.edit-button {
  background-color: blue;
}

.delete-button {
  background-color: red;
}

.submit-btn {
  background-color: green;
}

.cancel-btn {
  background-color: red;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.modal-buttons {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.modal input {
  width: 100%;
  padding: 6px;
  margin-top: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: white;
  color: black;
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
}
</style>
