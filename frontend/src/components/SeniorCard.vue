<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const props = defineProps(['senior']);

function viewMedications() {
  router.push({ name: 'SeniorMedications', params: { id: props.senior.id } });
}
function viewAppointments() {
  router.push({ name: 'SeniorAppointments', params: { id: props.senior.id } });
}
function viewEmergencyContacts() {
  router.push({ name: 'SeniorEmergencyContacts', params: { id: props.senior.id } });
}
</script>

<template>
  <div class="senior-card">
    <h3><strong>Name:</strong> {{ props.senior.name }}</h3>
    <p><strong>Age:</strong> {{ props.senior.age }}</p>
    <p><strong>Phone:</strong> {{ props.senior.phone }}</p>

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
