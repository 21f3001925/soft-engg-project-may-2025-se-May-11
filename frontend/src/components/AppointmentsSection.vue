<script setup>
import { computed } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import { Calendar, ChevronRight, MapPin, Clock, Shield, Users } from 'lucide-vue-next';

const scheduleStore = useScheduleStore();

const appointments = computed(() => scheduleStore.upcomingAppointments.slice(0, 2));
</script>

<template>
  <div class="mb-10 p-8 rounded-3xl shadow-xl border border-purple-100 bg-gradient-to-br from-white to-purple-50/30">
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center text-2xl font-bold">
        <span
          class="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 mr-4"
        >
          <Calendar class="w-6 h-6 text-white" />
        </span>
        <span>Appointments</span>
      </div>
    </div>
    <div class="text-purple-500 text-sm mb-6 ml-14">Your schedule looks great!</div>
    <div class="space-y-4">
      <div
        v-for="appt in appointments"
        :key="appt.id"
        class="group p-4 bg-white rounded-xl border border-gray-100 hover:border-purple-200 hover:shadow-sm transition-all duration-300"
      >
        <div class="flex items-center justify-between mb-3">
          <span
            class="px-3 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-xs font-semibold"
            >{{ appt.date }}</span
          >
          <div class="flex items-center space-x-1 text-purple-600">
            <Clock class="w-4 h-4" />
            <span class="text-sm font-medium">{{ appt.time }}</span>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-6 h-6 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full flex items-center justify-center">
            <Shield class="w-3 h-3 text-white" />
          </div>
          <span class="text-sm font-medium text-gray-900 group-hover:text-purple-700 transition-colors">{{
            appt.name
          }}</span>
        </div>
        <div class="flex items-center text-xs text-gray-500 mt-2 ml-8">
          <MapPin class="w-3 h-3 mr-1" />
          {{ appt.details }}
        </div>
      </div>
    </div>
    <router-link
      to="/appointments"
      class="mt-8 w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 hover:from-purple-100 hover:to-pink-100 transition-all duration-300 text-purple-700 font-semibold shadow-sm hover:scale-105 active:scale-100 focus:outline-none focus:ring-2 focus:ring-purple-300"
    >
      View Full Calendar
      <ChevronRight class="w-5 h-5" />
    </router-link>
  </div>
</template>
