import { createRouter, createWebHistory } from 'vue-router';
import AuthorizationForm from './components/AuthorizationForm.vue';
import RegistrationForm from './components/RegistrationForm.vue';
import ActivationForm from './components/ActivationForm.vue';
import PasswordResetForm from './components/PasswordResetForm.vue';
//import PasswordResetConfirmForm from './components/PasswordResetConfirmForm.vue';
import ProfileComponent from './components/ProfileComponent.vue';
import ProfileEditForm from './components/ProfileEditForm.vue';

const routes = [
  { path: '/login', component: AuthorizationForm },
  { path: '/registration', component: RegistrationForm },
  { path: '/registration/activation/:uid/:token', component: ActivationForm },
  { path: '/password_reset', component: PasswordResetForm },
//  { path: '/password_reset_confirm/:uid/:token', component: PasswordResetConfirmForm },
  { path: '/users/:username', component: ProfileComponent },
  { path: '/me/edit', component: ProfileEditForm },
  { path: '/', redirect: '/login' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;