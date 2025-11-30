<template>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm sticky-top px-4 py-3 recruiter-navbar">
    <div class="container-fluid">
      <!-- Brand -->
      <router-link to="/recruiter" class="navbar-brand fw-bold text-primary">
        Recruiter Dashboard
      </router-link>

      <!-- Toggler -->
      <button
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#recruiterNav"
        aria-controls="recruiterNav"
        aria-expanded="false"
      >
        <i class="bi bi-list fs-3 text-primary"></i>
      </button>

      <!-- Nav Links -->
      <div class="collapse navbar-collapse" id="recruiterNav">
        <ul class="navbar-nav mx-auto text-center">
          <li class="nav-item">
            <router-link to="/recruiter" class="nav-link" active-class="active">
              <i class="bi bi-speedometer2 me-2"></i> Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/recruiter/profile" class="nav-link" active-class="active">
              <i class="bi bi-person me-2"></i> Profile
            </router-link>
          </li>

          <!-- ✅ New Smart Candidate Tracker Nav Item -->
          <li class="nav-item">
            <router-link to="/recruiter/tracker" class="nav-link" active-class="active">
              <i class="bi bi-kanban me-2"></i> Tracker
            </router-link>
          </li>
        </ul>

        <!-- Icons / Right Side -->
<div class="d-flex align-items-center justify-content-center justify-content-lg-end gap-3 mt-3 mt-lg-0">
  <i class="bi bi-bell fs-5 text-primary position-relative notification-icon">
    <span class="badge bg-danger position-absolute top-0 start-100 translate-middle p-1 border border-light rounded-circle"></span>
  </i>

  <!-- Simple Logout Button -->
  <button
    class="btn btn-outline-danger btn-sm"
    type="button"
    @click="logout"
  >
    <i class="bi bi-box-arrow-right me-1"></i>
    Logout
  </button>
</div>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

import Swal from "sweetalert2";

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");

  Swal.fire({
    toast: true,
    position: "top-end",
    icon: "success",
    title: "Logged out successfully!",
    showConfirmButton: false,
    timer: 2000,
  });

  router.push("/login");
};


</script>

<style scoped>
.recruiter-navbar {
  backdrop-filter: blur(8px);
  z-index: 1000;
}

/* Nav links */
.nav-link {
  color: #495057;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 8px 14px;
}

.nav-link:hover {
  color: #0072ff;
  background-color: rgba(0, 114, 255, 0.08);
}

.nav-link.active {
  background-color: rgba(0, 114, 255, 0.1);
  color: #0072ff !important;
  font-weight: 600;
}

/* Add space between nav items on large screens only */
@media (min-width: 992px) {
  .navbar-nav .nav-item + .nav-item {
    margin-left: 20px;
  }
}

/* Notification dot */
.notification-icon .badge {
  width: 8px;
  height: 8px;
}

/* Responsive */
@media (max-width: 992px) {
  .navbar-nav {
    margin-top: 1rem;
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 10px;
  }

  .nav-link {
    display: block;
    padding: 10px;
  }
}
</style>
