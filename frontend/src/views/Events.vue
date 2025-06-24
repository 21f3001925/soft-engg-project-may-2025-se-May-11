<script setup>
import { ref } from 'vue';

const events = ref([
  { id: 2, title: 'Yoga Class', date: '2025-06-16', location: 'Adyar', reminder: false },
  { id: 3, title: 'Community Meeting', date: '2025-06-20', location: 'T Nager', reminder: false },
]);

function markaRemainder(id) {
  console.log('Set a remainder button clicked', id);
}

function deleteEvent(id) {
  console.log('Delete event button clicked', id);
}

function addEvent() {
  console.log('Add new event button');
}
</script>

<template>
  <div class="events-page">
    <h1 style="text-align: center">Upcoming Events</h1>
    <div v-if="events.length === 0" class="no-events">
      <p>No upcoming events. Click below to add one!</p>
    </div>

    <div v-else class="event-grid">
      <div v-for="event in events" :key="event.id" class="event-card">
        <div class="event-details-grid">
          <div class="event-title">{{ event.title }}</div>
          <div class="event-date">{{ event.date }}</div>
          <div class="event-location">{{ event.location }}</div>
        </div>

        <div class="event-actions">
          <button class="set-remainder-button" @click="markaRemainder(event.id)">Set a Remainder</button>
          <button class="delete-button" @click="deleteEvent(event.id)">Delete</button>
        </div>
      </div>
    </div>

    <div class="action-bar">
      <button class="add-button" @click="addEvent">Add New Event</button>
    </div>
  </div>
</template>

<style scoped>
.events-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.events-page h1 {
  margin-bottom: 2rem;
  color: #1480be;
  font-size: 2rem;
}

.event-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background-color: rgb(251, 247, 247);
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(14, 14, 14, 0.1);
}

.event-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.event-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  color: black;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}

.event-details-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr; /* title, date, location */
  align-items: center;
  gap: 1rem;
}

.event-title,
.event-date,
.event-location {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-actions {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  margin-left: 1rem;
}

.reminder-button {
  background-color: #45ff07;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  color: #080808;
  cursor: pointer;
}

.delete-button {
  background-color: red;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-button {
  margin-top: 20px;
  background-color: rgb(81, 188, 231);
  color: black;
  padding: 10px 16px;
  border: none;
  border-radius: 5px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}
</style>
