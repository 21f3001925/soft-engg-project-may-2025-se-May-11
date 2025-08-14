<script setup>
import { defineProps, computed } from 'vue';
import { CheckCircle, Clock, Star } from 'lucide-vue-next';

const props = defineProps({
  med: {
    type: Object,
    required: true,
  },
  toggleMedication: {
    type: Function,
    required: true,
  },
});

const isOverdue = computed(() => {
  if (props.med.taken) return false;
  const now = new Date();
  const medTime = new Date(props.med.time);
  // Set the date of medTime to today's date for comparison
  medTime.setFullYear(now.getFullYear());
  medTime.setMonth(now.getMonth());
  medTime.setDate(now.getDate());
  return now > medTime;
});

const formattedTime = computed(() => {
  if (props.med.time) {
    const date = new Date(props.med.time);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  return '';
});
</script>

<template>
  <li
    class="flex items-center mb-2 py-3 px-4 rounded-xl bg-white border border-gray-100 transition-all duration-300 group relative overflow-hidden hover:bg-blue-50 hover:border-blue-200 hover:shadow-sm"
    :class="[med.taken ? 'bg-green-50 border-green-200' : '', isOverdue ? 'border-l-4 border-red-500' : '']"
  >
    <input
      :id="'med-' + med.id"
      type="checkbox"
      :checked="med.taken"
      class="w-4 h-4 accent-blue-500 mr-3 mt-1"
      title="Mark as taken"
      @change="() => toggleMedication(med.id)"
    />
    <div class="flex-1 min-w-0">
      <label
        :for="'med-' + med.id"
        class="block font-medium text-gray-900 transition-all duration-200 cursor-pointer"
        :class="med.taken ? 'text-gray-500 italic' : 'group-hover:text-blue-700'"
      >
        {{ med.name }}
      </label>
      <div class="flex items-center text-xs mt-1" :class="isOverdue && !med.taken ? 'text-red-500' : 'text-gray-500'">
        <Clock class="w-4 h-4 mr-1" />
        <span>{{ formattedTime }}</span>
        <span
          v-if="isOverdue && !med.taken"
          class="ml-2 px-2 py-0.5 rounded-full bg-red-100 text-red-600 font-semibold text-xs"
          >Overdue</span
        >
      </div>
    </div>
    <transition name="fade">
      <div v-if="med.taken" class="flex items-center ml-3 text-green-600">
        <Star class="w-4 h-4 fill-current mr-1" />
        <span class="text-xs font-medium">Done!</span>
      </div>
    </transition>
    <transition name="fade">
      <CheckCircle v-if="med.taken" class="ml-2 w-5 h-5 text-green-500" title="Taken!" />
    </transition>
  </li>
</template>
