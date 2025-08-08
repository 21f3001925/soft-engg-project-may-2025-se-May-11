import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import Medications from '../views/Medications.vue';
import Appointments from '../views/Appointments.vue';
import News from '../views/News.vue';
import Profile from '../views/Profile.vue';
import Events from '../views/Events.vue';
import Setting from '../views/Setting.vue';
import CaregiverDashboard from '../views/CaregiverDashboard.vue';
import SeniorMedications from '../views/SeniorMedications.vue';
import SeniorAppointments from '../views/SeniorAppointments.vue';
import SeniorEmergencyContacts from '../views/SeniorEmergencyContacts.vue';
import AccessibilitySettings from '../views/AccessibilitySettings.vue';
import ServiceProviderDashboard from '../views/ServiceProviderDashboard.vue';
import EmergencyContacts from '../views/EmergencyContacts.vue';

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
    path: '/medications/:id',
    name: 'Medications',
    component: Medications,
  },
  {
    path: '/appointments',
    name: 'Appointments',
    component: Appointments,
  },
  {
    path: '/news',
    name: 'News',
    component: News,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/emergency-contacts',
    name: 'EmergencyContacts',
    component: EmergencyContacts,
  },
  {
    path: '/events',
    name: 'Events',
    component: Events,
  },
  {
    path: '/setting',
    name: 'Setting',
    component: Setting,
  },
  {
    path: '/settings/notifications',
    name: 'notifications',
    component: Setting,
  },
  {
    path: '/settings/change-password',
    name: 'change-password',
    component: Setting,
  },
  {
    path: '/caregiver-dashboard',
    name: 'CaregiverDashboard',
    component: CaregiverDashboard,
  },
  {
    path: '/caregiver/seniors/:id/medications',
    name: 'SeniorMedications',
    component: SeniorMedications,
  },
  {
    path: '/caregiver/seniors/:id/appointments',
    name: 'SeniorAppointments',
    component: SeniorAppointments,
  },
  {
    path: '/caregiver/seniors/:id/emergency-contacts',
    name: 'SeniorEmergencyContacts',
    component: SeniorEmergencyContacts,
  },
  {
    path: '/settings/accessibility',
    name: AccessibilitySettings,
    component: AccessibilitySettings,
  },
  {
    path: '/service-provider',
    name: ServiceProviderDashboard,
    component: ServiceProviderDashboard,
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
