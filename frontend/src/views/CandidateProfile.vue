<template>
  <Navbar />

  <!-- Toast Container -->
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999;">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="glass-toast shadow-sm mb-2"
      :class="toast.type"
    >
      <div class="toast-icon">
        <i :class="toast.icon"></i>
      </div>
      <div class="toast-body">
        {{ toast.message }}
      </div>
    </div>
  </div>

  <section class="profile-section py-5">
    <div class="container">
      <div class="text-center mb-4 fade-in">
        <h2 class="fw-bold text-gradient">Candidate Profile</h2>
        <p class="text-muted">Update your educational and career details</p>
      </div>

      <div class="profile-card p-4 rounded-4 shadow-sm fade-in">
        <form @submit.prevent="saveProfile">

          <!-- FIRST NAME -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.firstname"
              type="text"
              id="firstname"
              class="form-control rounded-3 shadow-sm"
              placeholder="First Name"
              required
            />
            <label for="firstname">First Name</label>
          </div>

          <!-- LAST NAME -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.lastname"
              type="text"
              id="lastname"
              class="form-control rounded-3 shadow-sm"
              placeholder="Last Name"
              required
            />
            <label for="lastname">Last Name</label>
          </div>

          <!-- Email -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.email"
              type="email"
              id="email"
              class="form-control rounded-3 shadow-sm"
              placeholder="Email"
              required
            />
            <label for="email">Email</label>
          </div>

          <!-- Age -->
          <div class="form-floating mb-3">
            <input
              v-model.number="profile.age"
              type="number"
              id="age"
              class="form-control rounded-3 shadow-sm"
              placeholder="Age"
              min="18"
              required
            />
            <label for="age">Age</label>
          </div>

          <!-- Education -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.education"
              type="text"
              id="education"
              class="form-control rounded-3 shadow-sm"
              placeholder="Education"
              required
            />
            <label for="education">Education</label>
          </div>

          <!-- Resume -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Resume</label>
            <input
              type="file"
              @change="handleFileUpload"
              class="form-control rounded-3 shadow-sm"
            />
            <small v-if="profile.resume" class="text-muted">
              Current: {{ profile.resume }}
            </small>
          </div>

          <div class="text-end mt-4">
            <button
              type="submit"
              class="btn btn-gradient rounded-3 shadow-sm px-4 py-2"
              :disabled="isSaving"
            >
              <i v-if="isSaving" class="bi bi-hourglass-split me-2"></i>
              <i v-else class="bi bi-save me-2"></i>
              {{ isSaving ? "Saving..." : "Save Changes" }}
            </button>
          </div>

        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/CandidateNavbar.vue";

const API_URL = "http://127.0.0.1:5000/api";
const token = localStorage.getItem("token");

// ----------------------
// Profile State
// ----------------------
const profile = ref({
  firstname: "",
  lastname: "",
  email: "",
  age: "",
  education: "",
  resume: "",
});

const selectedResumeFile = ref(null);
const isSaving = ref(false);

// ----------------------
// Toast System
// ----------------------
const toasts = ref([]);

const toastSound = new Audio("/sounds/notify.mp3");

function showToast(message, type = "info") {
  const id = Date.now();
  const icon =
    type === "success"
      ? "bi bi-check-circle-fill text-success"
      : type === "error"
      ? "bi bi-x-circle-fill text-danger"
      : "bi bi-info-circle-fill text-primary";

  toasts.value.push({ id, message, type, icon });

  toastSound.currentTime = 0;
  toastSound.play();

  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }, 4200);
}

// ----------------------
// Load Profile
// ----------------------
onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/index`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (data.success) {
      const user = data.user;

      profile.value.firstname = user.firstname;
      profile.value.lastname = user.lastname;
      profile.value.email = user.email;
      profile.value.age = user.candidate.age;
      profile.value.education = user.candidate.education;
      profile.value.resume =
        user.candidate.resume_file_path?.split("\\").pop() || "";
    }
  } catch (err) {
    showToast("Failed to load profile", "error");
  }
});

// ----------------------
// File Upload Handler
// ----------------------
function handleFileUpload(e) {
  selectedResumeFile.value = e.target.files[0];
}

// ----------------------
// SAVE PROFILE
// Includes triggering resume parsing
// ----------------------
async function saveProfile() {
  if (profile.value.age < 18) {
    showToast("Age must be at least 18", "error");
    return;
  }

  isSaving.value = true;

  try {
    const formData = new FormData();

    formData.append("user_data", JSON.stringify({
      firstname: profile.value.firstname,
      lastname: profile.value.lastname,
      email: profile.value.email,
      education: profile.value.education,
      age: profile.value.age,
    }));

    if (selectedResumeFile.value) {
      formData.append("file", selectedResumeFile.value);
    }

    const res = await fetch(`${API_URL}/update-candidate`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Update failed");

    showToast("Profile updated", "success");
    localStorage.setItem("firstname", profile.value.firstname);
    // ------------------------------
    // NEW — RESUME PARSING STARTED
    // ------------------------------
    if (data.parsing_started) {
      showToast("New resume uploaded. Parsing started...", "info");

      setTimeout(checkParsingResult, 2000);
    }

  } catch (err) {
    showToast(err.message, "error");
  }

  isSaving.value = false;
}


async function checkParsingResult() {
  try {
    const res = await fetch(`${API_URL}/resume-status`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();
    const status = data.status;

    if (status === "SUCCESS") {
      showToast("Resume parsed successfully!", "success");
      return;
    }

    if (status === "FAILED") {
      showToast("Resume parsing failed", "error");
      return;
    }

    // If still PENDING or PROCESSING → wait & check again
    setTimeout(checkParsingResult, 2000);

  } catch (err) {
    console.error(err);
  }
}


// ----------------------
// CHECK PARSING STATUS ONCE
// ----------------------
async function checkParsingStatusOnce() {
  try {
    const res = await fetch(`${API_URL}/resume-status`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();
    const status = data.status?.toUpperCase();

    if (status === "SUCCESS") {
      showToast("Resume parsed successfully!", "success");
    } else if (status === "FAILED") {
      showToast("Resume parsing failed", "error");
      showRetryPopup();
    }
  } catch (err) {
    console.error(err);
  }
}

// ----------------------
// RETRY POPUP
// ----------------------
function showRetryPopup() {
  const retry = confirm("Resume parsing failed. Retry?");
  if (retry) retryParsing();
}

// Retry request
async function retryParsing() {
  try {
    const res = await fetch(`${API_URL}/resume-retry`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (res.ok) {
      showToast("Retry started", "info");
      setTimeout(checkParsingStatusOnce, 1500);
    }
  } catch (err) {
    showToast("Retry failed", "error");
  }
}
</script>

<style scoped>
/* Glass Toast */
.glass-toast {
  display: flex;
  align-items: center;
  min-width: 260px;
  padding: 12px 15px;
  border-radius: 14px;
  backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.8);
  animation: fadeSlide 0.45s ease;
}

.glass-toast .toast-icon {
  font-size: 1.4rem;
  margin-right: 10px;
}

.glass-toast.success {
  border-left: 5px solid #28a745;
}
.glass-toast.error {
  border-left: 5px solid #dc3545;
}
.glass-toast.info {
  border-left: 5px solid #0d6efd;
}

.btn-gradient {
  background: linear-gradient(90deg, #913ee3ff, #c33dd4ff);
  color: white;
  border: none;
}

.btn-gradient:hover {
  background: linear-gradient(90deg, #7f00ff, #e100ff);
  box-shadow: 0 4px 14px rgba(126, 0, 255, 0.3);
}


@keyframes fadeSlide {
  from {
    opacity: 0;
    transform: translateX(40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Background */
.profile-section {
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
}

/* Glassmorphism Card */
.profile-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
