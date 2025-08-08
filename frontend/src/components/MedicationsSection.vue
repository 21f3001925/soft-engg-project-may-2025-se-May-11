<script setup>
import { computed } from 'vue';
import { useScheduleStore } from '../store/scheduleStore';
import { useUserStore } from '../store/userStore';
import MedicationItem from './MedicationItem.vue';
import { Pill, ChevronRight } from 'lucide-vue-next';

const scheduleStore = useScheduleStore();
const userStore = useUserStore();

const seniorId = computed(() => userStore.user.id);

function toggleMedication(id) {
  const med = scheduleStore.medications.find((m) => m.id === id);
  if (med) {
    med.taken = !med.taken;
  }
}

const completedMeds = computed(() => scheduleStore.medications.filter((med) => med.taken).length);
const totalMeds = computed(() => scheduleStore.medications.length);
const progressPercentage = computed(() => (totalMeds.value === 0 ? 0 : (completedMeds.value / totalMeds.value) * 100));
</script>

<template>
  <div class="mb-10 p-8 rounded-3xl shadow-xl border border-blue-100 bg-gradient-to-br from-white to-blue-50/30 h-full">
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center text-2xl font-bold">
        <span
          class="w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-r from-blue-500 to-blue-600 mr-4"
        >
          <Pill class="w-6 h-6 text-white" />
        </span>
        <span>Medications</span>
      </div>
      <span class="px-4 py-1 rounded-full bg-blue-100 text-blue-700 text-base font-semibold"
        >{{ completedMeds }}/{{ totalMeds }}</span
      >
    </div>
    <div class="text-gray-500 text-sm mb-6 ml-14">Your daily medication schedule</div>
    <div class="mb-6 ml-14">
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm text-gray-600">Daily Progress</span>
        <span class="text-xs text-blue-700 font-semibold">{{ Math.round(progressPercentage) }}%</span>
      </div>
      <div class="w-full h-3 bg-blue-100 rounded-full overflow-hidden">
        <div
          class="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full transition-all duration-500"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
    </div>
    <div class="border-t border-gray-200 my-6"></div>
    <ul>
      <MedicationItem
        v-for="med in scheduleStore.medications"
        :key="med.id"
        :med="med"
        :toggleMedication="toggleMedication"
      />
    </ul>
    <router-link
      :to="`/medications/${seniorId}`"
      class="mt-8 w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 hover:from-blue-100 hover:to-purple-100 transition-all duration-300 text-blue-700 font-semibold shadow-sm hover:scale-105 active:scale-100 focus:outline-none focus:ring-2 focus:ring-blue-300"
    >
      View All Medications
      <ChevronRight class="w-5 h-5" />
    </router-link>
  </div>
</template>

<style scoped>
.progress-bar-container {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  margin-top: 4px;
}
.progress-bar {
  background: #4f8cff;
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}
</style>
