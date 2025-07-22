<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import mockApiService from '../services/mockApiService';
import { Mail, Phone } from 'lucide-vue-next';

const router = useRouter();
const loginMethod = ref('email');
const email = ref('');
const phone = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

function handleGoogleSignIn() {
  alert('Google sign-in coming soon!');
}

const handleLogin = async () => {
  error.value = '';
  loading.value = true;
  try {
    const response = await mockApiService.login();
    if (response.status === 200) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      router.push('/dashboard');
    }
  } catch (err) {
    error.value = 'Invalid credentials';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div
    class="flex-1 flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-purple-100 py-20 px-4"
  >
    <div class="w-full max-w-md p-8 rounded-3xl shadow-xl border border-blue-100 bg-white/90">
      <div class="mb-8 text-center">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-1">
          Welcome
        </h2>
        <p class="text-sm text-gray-500">Sign in to your SeniorCare dashboard</p>
      </div>
      <button
        @click="handleGoogleSignIn"
        class="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl border-2 border-gray-200 bg-white shadow-md hover:bg-gray-50 hover:border-blue-400 transition-all duration-200 font-bold text-base text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-300 mb-6"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" class="w-5 h-5">
          <g>
            <path
              fill="#4285F4"
              d="M24 9.5c3.54 0 6.7 1.22 9.19 3.23l6.85-6.85C35.64 2.7 30.18 0 24 0 14.82 0 6.71 5.82 2.69 14.09l7.98 6.2C12.13 13.13 17.57 9.5 24 9.5z"
            />
            <path
              fill="#34A853"
              d="M46.1 24.55c0-1.64-.15-3.22-.42-4.74H24v9.01h12.42c-.54 2.9-2.18 5.36-4.65 7.01l7.19 5.6C43.98 37.13 46.1 31.3 46.1 24.55z"
            />
            <path
              fill="#FBBC05"
              d="M10.67 28.29a14.5 14.5 0 0 1 0-8.58l-7.98-6.2A23.94 23.94 0 0 0 0 24c0 3.77.9 7.34 2.69 10.49l7.98-6.2z"
            />
            <path
              fill="#EA4335"
              d="M24 48c6.18 0 11.36-2.05 15.15-5.59l-7.19-5.6c-2.01 1.35-4.6 2.16-7.96 2.16-6.43 0-11.87-3.63-14.33-8.79l-7.98 6.2C6.71 42.18 14.82 48 24 48z"
            />
            <path fill="none" d="M0 0h48v48H0z" />
          </g>
        </svg>
        <span>Continue with Google</span>
      </button>
      <div class="flex items-center my-6">
        <div class="flex-grow h-px bg-gray-200"></div>
        <span class="mx-4 text-gray-400 font-semibold">or</span>
        <div class="flex-grow h-px bg-gray-200"></div>
      </div>
      <div class="mb-2 text-sm font-medium text-gray-600">Sign in with:</div>
      <div
        class="flex mb-2 rounded-t-xl overflow-hidden border border-blue-100 bg-blue-50"
        role="tablist"
        aria-label="Login method"
      >
        <button
          class="w-1/2 py-2 text-base font-bold flex items-center justify-center gap-1 transition-all duration-200 focus:outline-none border-b-4 rounded-t-xl"
          :class="
            loginMethod === 'email'
              ? 'bg-blue-600 text-white border-blue-700 scale-105 shadow-lg z-10'
              : 'bg-transparent text-gray-500 border-gray-200 hover:bg-blue-100 hover:text-blue-700 hover:border-blue-400 hover:shadow'
          "
          @click="loginMethod = 'email'"
          role="tab"
          :aria-selected="loginMethod === 'email'"
          aria-controls="email-panel"
        >
          <Mail class="w-5 h-5 mr-1" /> Email
        </button>
        <button
          class="w-1/2 py-2 text-base font-bold flex items-center justify-center gap-1 transition-all duration-200 focus:outline-none border-b-4 rounded-t-xl"
          :class="
            loginMethod === 'phone'
              ? 'bg-blue-600 text-white border-blue-700 scale-105 shadow-lg z-10'
              : 'bg-transparent text-gray-500 border-gray-200 hover:bg-blue-100 hover:text-blue-700 hover:border-blue-400 hover:shadow'
          "
          @click="loginMethod = 'phone'"
          role="tab"
          :aria-selected="loginMethod === 'phone'"
          aria-controls="phone-panel"
        >
          <Phone class="w-5 h-5 mr-1" /> Phone Number
        </button>
      </div>
      <div class="text-xs text-gray-500 mb-4 text-center">Choose how you want to sign in: Email or Phone Number.</div>
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div v-if="loginMethod === 'email'" id="email-panel" role="tabpanel">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            :disabled="loading"
            class="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-300 focus:border-blue-400 transition text-base bg-white"
            autocomplete="email"
            placeholder="e.g. name@example.com"
          />
        </div>
        <div v-else id="phone-panel" role="tabpanel">
          <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
          <input
            id="phone"
            v-model="phone"
            type="tel"
            required
            :disabled="loading"
            pattern="^\d{10}$"
            class="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-300 focus:border-blue-400 transition text-base bg-white"
            autocomplete="tel"
            placeholder="e.g. 9876543210"
          />
          <span v-if="phone && !/^\d{10}$/.test(phone)" class="text-xs text-red-500"
            >Enter a valid 10-digit mobile number</span
          >
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            :disabled="loading"
            class="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-300 focus:border-blue-400 transition text-base bg-white"
            autocomplete="current-password"
          />
        </div>
        <div v-if="error" class="text-red-500 text-sm text-center">{{ error }}</div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold shadow-md hover:from-blue-600 hover:to-purple-600 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <div class="mt-6 text-center text-sm text-gray-500">
        Don't have an account?
        <router-link to="/register" class="text-blue-600 font-semibold hover:underline ml-1">Register</router-link>
      </div>
    </div>
  </div>
</template>
