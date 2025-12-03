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

          <!-- Email -->
          <div class="form-floating mb-3">
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': emailError }"
              placeholder="name@example.com"
            />
            <label for="email">Email Address</label>
            <div class="invalid-feedback small">{{ emailError }}</div>
          </div>

          <!-- Password -->
          <div class="form-floating mb-4">
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': passwordError }"
              placeholder="••••••••"
            />
            <label for="password">Password</label>
            <div class="invalid-feedback small">{{ passwordError }}</div>
          </div>

          <!-- Server Error -->
          <div v-if="serverError" class="alert alert-danger text-center small py-2 mb-3">
            {{ serverError }}
          </div>

          <!-- Login Button -->
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
          <router-link to="/signup" class="fw-semibold text-gradient text-decoration-none">
            Sign Up
          </router-link>
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import { ref, watch } from "vue";
import Swal from "sweetalert2";
import { useRouter } from "vue-router";

const router = useRouter();

// -------------------------------------------
// STATE
// -------------------------------------------
const email = ref("");
const password = ref("");

// ERRORS
const emailError = ref("");
const passwordError = ref("");
const serverError = ref("");

// UI
const isLoading = ref(false);

const API_URL = "http://127.0.0.1:5000";

// -------------------------------------------
// LIVE ERROR CLEARING
// -------------------------------------------
watch(email, (v) => {
  if (v.includes("@")) emailError.value = "";
});

watch(password, (v) => {
  if (v.length >= 6) passwordError.value = "";
});

// -------------------------------------------
// HANDLE LOGIN
// -------------------------------------------
const handleLogin = async () => {
  emailError.value = "";
  passwordError.value = "";
  serverError.value = "";

  let valid = true;

  if (!email.value.includes("@")) {
    emailError.value = "Please enter a valid email address.";
    valid = false;
  }

  if (password.value.length < 6) {
    passwordError.value = "Password must be at least 6 characters.";
    valid = false;
  }

  if (!valid) return;

  isLoading.value = true;

  try {
    const response = await fetch(`${API_URL}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email.value.trim(),
        password: password.value
      })
    });

    const data = await response.json();

    // Handle API errors
    if (!response.ok || !data.success) {
      serverError.value = data.message || "Invalid email or password.";
      setTimeout(() => (serverError.value = ""), 3000);
      isLoading.value = false;
      return;
    }

    // -------------------------------------------
    // SAVE TOKEN + USER INFO
    // -------------------------------------------
    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.user.role);
    localStorage.setItem("user_id", data.user.id);
    localStorage.setItem("firstname", data.user.firstname);

    Swal.fire({
      toast: true,
      position: "top-end",
      icon: "success",
      title: "Login successful!",
      showConfirmButton: false,
      timer: 2000,
    });

    // -------------------------------------------
    // REDIRECT ACCORDING TO ROLE
    // -------------------------------------------
    if (data.user.role === "CANDIDATE") {
      router.push("/candidate");
    } else if (data.user.role === "RECRUITER") {
      router.push("/recruiter");
    } else {
      router.push("/");
    }

  } catch (err) {
    serverError.value = "Server error. Please try again later.";
  }

  isLoading.value = false;
};
</script>

<style scoped>
/* Background same as Signup */
.login-container {
  min-height: calc(100vh - 80px);
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
  backdrop-filter: blur(10px);
}

/* Card */
.login-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  max-width: 460px;
  width: 100%;
  transition: 0.3s ease;
}

.login-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 114, 255, 0.15);
}

/* Inputs */
.form-control {
  height: 48px !important;
  font-size: 15px;
  border-radius: 12px !important;
  border: 1.5px solid #d4d9e1;
  transition: all 0.2s ease-in-out;
}

.form-control:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 0.15rem rgba(0, 114, 255, 0.20);
}

/* Gradient Title */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Gradient Button */
.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: white;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 114, 255, 0.25);
}

/* Shake animation */
.is-invalid {
  border-color: #ff4d4f !important;
  animation: shake 0.2s ease-in-out;
}

@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-3px); }
  50% { transform: translateX(3px); }
  75% { transform: translateX(-3px); }
  100% { transform: translateX(0); }
}
</style>
