// src/router/index.js
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
      component: () => import('../views/SmartCandidateTracker.vue'),
    },
    {
      path: '/candidate',
      name: 'candidate-dashboard',
      component: () => import('../views/CandidateDashboard.vue'),
    },
    {
      path: '/candidate/profile',
      name: 'candidate-profile',
      component: () => import('../views/CandidateProfile.vue'),
    },
    {
      path: '/candidate/saved',
      name: 'candidate-saved-jobs',
      component: () => import('../views/SavedJobs.vue'),
    },
    // ENABLED: applied jobs view (single file view you asked for earlier)
    {
      path: '/candidate/applied/:id?',
      name: 'candidate-applied-jobs',
      component: () => import('../views/AppliedJobs.vue'),
      // :id? is optional — useful later for deep-linking to an application
    },
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  // Public pages (no auth needed) — use a Set for membership checks
  const publicPages = new Set(['/', '/login', '/signup', '/about', '/contact', '/jobs']);

  if (publicPages.has(to.path)) {
    return next();
  }

  if (!token) {
    return next('/login');
  }

  // Role-based access
  if (to.path.startsWith('/candidate') && role !== 'CANDIDATE') {
    return next('/login');
  }

  if (to.path.startsWith('/recruiter') && role !== 'RECRUITER') {
    return next('/login');
  }

  next();
});

export default router;
