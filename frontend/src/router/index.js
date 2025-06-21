import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import Medications from '../views/Medications.vue';
import Appointments from '../views/Appointments.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/medications',
    name: 'Medications',
    component: Medications,
  },
  {
    path: '/appointments',
    name: 'Appointments',
    component: Appointments,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');
  const isPublicRoute = to.matched.some((record) => record.meta.requiresAuth === false);

  if (!isPublicRoute && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
