<template>

  <Navbar />

  <div class="login-container d-flex justify-content-center align-items-center py-5">
    <div class="login-card shadow-lg p-4 p-md-5">
      <div class="card-body">
        <!-- Title -->
        <h2 class="text-center fw-bold text-gradient mb-3">Welcome Back 👋</h2>
        <p class="text-center text-muted mb-4">
          Log in to continue your journey with <span class="fw-semibold">ApplAI</span>.
        </p>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" novalidate>
          <div class="mb-3">
            <label for="email" class="form-label fw-semibold">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-control form-control-lg rounded-3 shadow-sm"
              :class="{ 'is-invalid': emailError }"
              placeholder="name@example.com"
              required
            />
            <div class="invalid-feedback small">{{ emailError }}</div>
          </div>

          <div class="mb-4">
            <label for="password" class="form-label fw-semibold">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control form-control-lg rounded-3 shadow-sm"
              :class="{ 'is-invalid': passwordError }"
              placeholder="••••••••"
              required
            />
            <div class="invalid-feedback small">{{ passwordError }}</div>
          </div>

          <div v-if="serverError" class="alert alert-danger text-center small py-2 mb-3">
            {{ serverError }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-gradient w-100 py-2 fw-bold rounded-3 shadow-sm"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Logging In...' : 'Log In' }}
          </button>
        </form>

        <!-- Signup Redirect -->
        <p class="text-center mt-4 small text-muted">
          Don’t have an account?
          <router-link
            to="/signup"
            class="fw-semibold text-gradient text-decoration-none"
          >
            Sign Up
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const emailError = ref("");
const passwordError = ref("");
const serverError = ref("");
const isLoading = ref(false);

const handleLogin = () => {
  emailError.value = "";
  passwordError.value = "";
  serverError.value = "";

  if (!email.value.includes("@")) {
    emailError.value = "Please enter a valid email address.";
    return;
  }
  if (password.value.length < 6) {
    passwordError.value = "Password must be at least 6 characters.";
    return;
  }

  isLoading.value = true;
  setTimeout(() => {
    isLoading.value = false;
    if (email.value === "test@jobportal.com" && password.value === "password") {
      router.push("/");
    } else {
      serverError.value = "Invalid email or password. Please try again.";
    }
  }, 1500);
};
</script>

<style scoped>
/* Background matches Home aesthetic */
.login-container {
  min-height: calc(100vh - 80px);
  background: linear-gradient(120deg, #f3f6ff, #e9f2ff);
  backdrop-filter: blur(10px);
}

/* Card with glass effect */
.login-card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 114, 255, 0.1);
  border-radius: 1.25rem;
  max-width: 440px;
  width: 100%;
  transition: all 0.3s ease;
}

.login-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 114, 255, 0.1);
}

/* Text gradient for brand feel */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Inputs */
.form-control {
  border: 1.5px solid #dee2e6;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 0.15rem rgba(0, 114, 255, 0.15);
}

/* Gradient Button */
.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff;
  border: none;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  background: linear-gradient(90deg, #00a2ff, #0072ff);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 114, 255, 0.25);
}

/* Small elements */
.text-muted {
  color: #6c757d !important;
}

/* Smooth hover effect for link */
a.text-gradient:hover {
  opacity: 0.8;
}
</style>
