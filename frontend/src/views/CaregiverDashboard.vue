<script setup>
import { onMounted, ref } from 'vue';
import { useCaregiverStore } from '../store/caregiverStore';
import SeniorCard from '../components/SeniorCard.vue';

const caregiverStore = useCaregiverStore();
const loading = ref(true);
const selectedSenior = ref('');
const assignError = ref('');
const showAssignModal = ref(false);

onMounted(async () => {
  await caregiverStore.fetchAssignedSeniors();
  await caregiverStore.fetchAvailableSeniors();
  loading.value = false;
});

function openAssignModal() {
  showAssignModal.value = true;
  assignError.value = '';
  selectedSenior.value = '';
}

async function assignSenior() {
  if (!selectedSenior.value) return;
  assignError.value = '';
  try {
    await caregiverStore.assignCaregiverToSenior(selectedSenior.value);
    selectedSenior.value = '';
    showAssignModal.value = false;
    await caregiverStore.fetchAssignedSeniors();
    await caregiverStore.fetchAvailableSeniors();
  } catch (err) {
    assignError.value = err.response?.data?.message || err.message || 'Failed to assign caregiver';
  }
}
</script>

<template>
  <div class="dashboard caregiver-dashboard max-w-7xl mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
      <div class="col-span-1 md:col-span-3">
        <div
          class="flex items-center justify-between mb-8 p-6 rounded-2xl shadow bg-gradient-to-r from-green-100 via-white to-blue-100 border border-green-50"
        >
          <div>
            <h2
              class="dashboard-title text-2xl md:text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-1"
            >
              Caregiver Dashboard
            </h2>
            <p class="text-xs text-gray-500 hidden md:block">Manage your assigned senior citizens</p>
          </div>

          <div class="flex items-center space-x-2 bg-white/80 rounded-full px-4 py-2 shadow border border-gray-100">
            <span class="text-lg font-mono text-gray-700">{{
              new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }}</span>
          </div>
        </div>
      </div>

      <div class="col-span-1 md:col-span-3">
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          <span class="ml-3 text-gray-600">Loading seniors...</span>
        </div>

        <!-- Assignment UI: show inline only if no seniors assigned -->
        <div
          v-else-if="caregiverStore.assignedSeniors.length === 0"
          class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8"
        >
          <div class="text-center">
            <div
              class="w-24 h-24 bg-gradient-to-br from-green-100 to-blue-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg"
            >
              <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
                ></path>
              </svg>
            </div>
            <h3 class="text-2xl font-semibold text-gray-900 mb-3">Assign yourself to a Senior Citizen</h3>
            <p class="text-gray-600 mb-8 max-w-md mx-auto">
              Get started by assigning yourself to a senior citizen to begin providing care and support.
            </p>

            <div v-if="caregiverStore.availableSeniors.length === 0" class="text-gray-500 mb-6">
              No unassigned seniors available.
            </div>
            <div v-else class="max-w-md mx-auto">
              <select
                v-model="selectedSenior"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-colors mb-4"
              >
                <option disabled value="">Select a senior</option>
                <option v-for="senior in caregiverStore.availableSeniors" :key="senior.id" :value="senior.id">
                  {{ senior.name }} ({{ senior.email }})
                </option>
              </select>
              <button
                @click="assignSenior"
                :disabled="!selectedSenior"
                class="w-full px-8 py-4 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Assign Senior
              </button>
            </div>
            <div v-if="assignError" class="mt-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
              {{ assignError }}
            </div>
          </div>
        </div>

        <!-- "Assign another senior" button and modal, shown if at least one assigned -->
        <div v-else class="space-y-6">
          <div class="flex justify-end">
            <button
              class="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-semibold"
              @click="openAssignModal"
            >
              Assign Another Senior
            </button>
          </div>

          <!-- Dashboard for assigned seniors -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SeniorCard
              v-for="senior in caregiverStore.assignedSeniors"
              :key="senior.id"
              :senior="senior"
              @remove="() => caregiverStore.removeCaregiverFromSenior(senior.id)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for assignment -->
    <div v-if="showAssignModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-900">Assign Another Senior</h3>
            <button @click="showAssignModal = false" class="text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div v-if="caregiverStore.availableSeniors.length === 0" class="text-center py-8 text-gray-500">
            No unassigned seniors available.
          </div>
          <div v-else class="space-y-4">
            <select
              v-model="selectedSenior"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-colors"
            >
              <option disabled value="">Select a senior</option>
              <option v-for="senior in caregiverStore.availableSeniors" :key="senior.id" :value="senior.id">
                {{ senior.name }} ({{ senior.email }})
              </option>
            </select>
            <div class="flex gap-3 pt-4">
              <button
                @click="assignSenior"
                :disabled="!selectedSenior"
                class="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg hover:from-green-600 hover:to-blue-600 transition-all duration-200 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Assign
              </button>
              <button
                @click="showAssignModal = false"
                class="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition-colors font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
          <div v-if="assignError" class="mt-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
            {{ assignError }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
}
</style>
