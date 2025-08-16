<template>
  <div class="report-analyzer-container p-8">
    <h1 class="text-3xl font-bold mb-6">AI Report Analyzer</h1>

    <!-- Report Analyzer Content -->
    <div class="tab-content mt-6">
      <div class="upload-section bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4">Upload Your Report</h2>
        <p class="mb-4">Upload a PDF or image file to get an AI-powered summary and ask questions.</p>

        <div class="flex items-center space-x-4">
          <input type="file" @change="handleFileUpload" accept=".pdf,.png,.jpg,.jpeg" class="file-input" />
          <button @click="submitReport" :disabled="!file || loading" class="btn-primary">
            <span v-if="loading">Analyzing...</span>
            <span v-else>Analyze Report</span>
          </button>
        </div>
      </div>

      <div v-if="error" class="error-message mt-6 p-4 bg-red-100 text-red-700 rounded-lg">
        <p class="font-bold">Error:</p>
        <p>{{ error }}</p>
      </div>

      <div v-if="summary" class="summary-section mt-6 bg-white p-6 rounded-lg shadow-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-semibold">Summary</h2>
          <button @click="downloadSummary" class="btn-secondary">Download Summary</button>
        </div>
        <p class="text-gray-700 whitespace-pre-wrap">{{ summary }}</p>
      </div>

      <!-- Chatbot Section -->
      <Chatbot v-if="reportId" :report-id="reportId" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import reportService from '../services/reportService';
import Chatbot from '../components/Chatbot.vue';

// --- Report Analyzer State ---
const file = ref(null);
const summary = ref('');
const loading = ref(false);
const error = ref('');
const reportId = ref(null);

// --- Report Analyzer Methods ---
const handleFileUpload = (event) => {
  file.value = event.target.files[0];
  error.value = '';
  summary.value = '';
  reportId.value = null;
};

const submitReport = async () => {
  if (!file.value) {
    error.value = 'Please select a file first.';
    return;
  }

  loading.value = true;
  error.value = '';
  summary.value = '';
  reportId.value = null;

  try {
    const response = await reportService.uploadReport(file.value);
    if (response.data && response.data.report) {
      summary.value = response.data.report.summary;
      reportId.value = response.data.report.report_id;
    } else {
      error.value = 'Failed to get a summary from the server.';
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'An unknown error occurred.';
  } finally {
    loading.value = false;
  }
};

const downloadSummary = async () => {
  if (!reportId.value) return;
  try {
    const response = await reportService.downloadReport(reportId.value);
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `summary-${reportId.value}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    error.value = 'Could not download the summary.';
  }
};
</script>

<style scoped>
.report-analyzer-container {
  max-width: 800px;
  margin: 0 auto;
}

.btn-primary {
  @apply bg-blue-500 text-white font-bold py-2 px-4 rounded;
}

.btn-primary:disabled {
  @apply bg-gray-400 cursor-not-allowed;
}

.btn-secondary {
  @apply bg-green-500 text-white font-bold py-2 px-4 rounded;
}

.file-input {
  @apply block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none;
}
</style>
