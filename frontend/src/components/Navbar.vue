<template>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm sticky-top border-bottom nav-glass">
    <div class="container-lg">
      <!-- Brand -->
      <router-link to="/" class="navbar-brand fw-bold fs-4 text-gradient">
        Appl<span class="text-dark">AI</span>
      </router-link>

      <!-- Toggler -->
      <button
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Nav Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item">
            <router-link to="/jobs" class="nav-link">Browse Jobs</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">About Us</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/contact" class="nav-link">Contact</router-link>
          </li>
        </ul>

        <!-- Buttons -->
        <div class="d-flex align-items-center">
          <router-link to="/login" class="btn btn-outline-primary me-2 rounded-3 nav-btn-outline shadow-sm">
            Log In
          </router-link>
          <router-link to="/signup" class="btn btn-primary rounded-3 nav-btn-filled shadow-sm">
            Sign Up
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
/* Glass effect */
.nav-glass {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.9);
}

/* Brand gradient */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Nav links */
.nav-link {
  color: #495057 !important;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 8px 14px;
}

.nav-link:hover {
  color: #0072ff !important;
  background-color: rgba(0, 114, 255, 0.08);
}

.nav-link.router-link-active {
  color: #0072ff !important;
  font-weight: 600;
  background-color: rgba(0, 114, 255, 0.1);
}

/* Outline Log In button */
.nav-btn-outline {
  color: #0072ff;
  border: 1.5px solid #0072ff;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-btn-outline:hover {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 114, 255, 0.3);
}

/* Filled Sign Up button */
.nav-btn-filled {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  border: none;
  color: #fff;
  transition: all 0.3s ease;
}

.nav-btn-filled:hover {
  background: linear-gradient(90deg, #00a2ff, #0072ff);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 114, 255, 0.3);
}

/* Toggler */
.navbar-toggler {
  transition: transform 0.3s ease;
}
.navbar-toggler:active {
  transform: rotate(90deg);
}

/* Responsive */
@media (max-width: 991px) {
  .navbar-nav {
    text-align: center;
    margin-top: 1rem;
  }
}

@media (min-width: 992px) {
  .navbar-nav .nav-item:not(:last-child) {
    margin-right: 1.5rem;
  }
}

</style>
