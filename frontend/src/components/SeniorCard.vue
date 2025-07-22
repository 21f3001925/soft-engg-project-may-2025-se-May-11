<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const senior = defineProps(['senior']);

function viewMedications() {
  router.push({ name: 'SeniorMedications', params: { id: senior.senior.id } });
}
function viewAppointments() {
  router.push({ name: 'SeniorAppointments', params: { id: senior.senior.id } });
}
function viewEmergencyContacts() {
  router.push({ name: 'SeniorEmergencyContacts', params: { id: senior.senior.id } });
}
</script>

<template>
  <div class="senior-card">
    <h3><strong>Name:</strong> {{ senior.senior.name }}</h3>
    <p><strong>Age:</strong> {{ senior.senior.age }}</p>
    <p><strong>Phone:</strong> {{ senior.senior.phone }}</p>

    <div class="actions">
      <button @click="viewMedications">Manage Medications</button>
      <button @click="viewAppointments">Manage Appointments</button>
      <button @click="viewEmergencyContacts">Manage Emergency Contacts</button>
    </div>
  </div>
</template>

<style scoped>
.senior-card {
  background: rgb(236, 196, 143);
  text-decoration-color: black;
  padding: 1.2rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-size: 18px;
}

.actions {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.5rem 0.5rem;
  border: none;
  background: #c218b9;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #2980b9;
}
</style>
