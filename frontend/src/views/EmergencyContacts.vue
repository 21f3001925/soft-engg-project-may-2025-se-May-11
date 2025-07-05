<script setup>
import { ref } from 'vue';
import { useUserStore } from '../store/userStore';

const userStore = useUserStore();

const contacts = ref(Object.entries(userStore.friends).map(([name, number]) => ({ name, number })));

const showModal = ref(false);
const selectedName = ref('');
const selectedNumber = ref('');
const isEdit = ref(false);
const editIndex = ref(null);
const toastMessage = ref('');

function addContact() {
  selectedName.value = '';
  selectedNumber.value = '';
  isEdit.value = false;
  showModal.value = true;
}

function editContact(index) {
  selectedName.value = contacts.value[index].name;
  selectedNumber.value = String(contacts.value[index].number);
  isEdit.value = true;
  editIndex.value = index;
  showModal.value = true;
}

function deleteContact(index) {
  contacts.value.splice(index, 1);
  showToast('Contact deleted');
}

function handleSubmit() {
  if (selectedName.value.trim() === '' || selectedNumber.value.trim() === '') {
    showToast('Name and number are required');
    return;
  }

  const newContact = { name: selectedName.value, number: selectedNumber.value };

  if (isEdit.value) {
    contacts.value[editIndex.value] = newContact;
    showToast('Contact updated');
  } else {
    contacts.value.push(newContact);
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

    <div v-if="contacts.length === 0" class="empty">No contacts added yet.</div>

    <ul v-else class="contact-list">
      <li v-for="(contact, index) in contacts" :key="index" class="contact-item">
        <span>{{ contact.name }} - {{ contact.number }}</span>
        <div class="buttons">
          <button class="edit-button" @click="editContact(index)">Edit</button>
          <button class="delete-button" @click="deleteContact(index)">Delete</button>
        </div>
      </li>
    </ul>

    <button class="add-btn" @click="addContact">Add Contact</button>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>{{ isEdit ? 'Edit Contact' : 'Add Contact' }}</h3>
        <input v-model="selectedName" placeholder="Enter contact name" />
        <input v-model="selectedNumber" placeholder="Enter contact number" />
        <div class="modal-buttons">
          <button class="submit-btn" @click="handleSubmit">{{ isEdit ? 'Update' : 'Add' }}</button>
          <button class="cancel-btn" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>

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
