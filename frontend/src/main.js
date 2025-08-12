import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import { createPinia } from 'pinia';
import router from './router';

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);

// Initialize user store to load accessibility settings
import { useUserStore } from './store/userStore';
const userStore = useUserStore();
userStore.initialize();

app.mount('#app');
