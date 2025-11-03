import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LogIn.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUp.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue'),
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/Contact.vue'),
    },
    {
      path: '/jobs',
      name: 'job',
      component: () => import('../views/JobListing.vue'),
    },
    {
      path: '/recruiter',
      name: 'recruiter-dashboard',
      component: () => import('../views/RecruiterDashboard.vue'),
    },
    {
      path: '/recruiter/profile',
      name: 'recruiter-profile',
      component: () => import('../views/RecruiterProfile.vue'),
    },
    {
      path: '/recruiter/tracker',
      name: 'SmartCandidateTracker',
      component: () => import('../views/SmartCandidateTracker.vue')
    },
    {
      path: '/candidate',
      name: 'candidate-dashboard',
      component: () => import('../views/CandidateDashboard.vue'),
    },
    {
      path: '/candidate/profile',
      name: 'candidate-profile',
      component: () => import('../views/CandidateProfile.vue')
    },
  ],
});

export default router;
