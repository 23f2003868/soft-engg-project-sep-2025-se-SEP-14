<template>
  <Navbar />

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
import Swal from "sweetalert2";

const API_URL = "http://127.0.0.1:5000";
const token = localStorage.getItem("token");

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

// Load candidate profile
onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/api/index`, {
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
    console.error("Failed to load profile", err);
  }
});

const handleFileUpload = (e) => {
  selectedResumeFile.value = e.target.files[0];
};

const saveProfile = async () => {
  if (profile.value.age < 18) {
    return Swal.fire("Invalid Age", "Age must be at least 18", "error");
  }

  isSaving.value = true;

  try {
    const formData = new FormData();

    const userData = {
      firstname: profile.value.firstname,
      lastname: profile.value.lastname,
      email: profile.value.email,
      education: profile.value.education,
      age: profile.value.age,
    };

    formData.append("user_data", JSON.stringify(userData));

    if (selectedResumeFile.value) {
      formData.append("file", selectedResumeFile.value);
    }

    const res = await fetch(`${API_URL}/api/update-candidate`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error);

    Swal.fire({
      icon: "success",
      title: "Profile Updated",
      text: "Your candidate profile was updated successfully!",
      timer: 2000,
      showConfirmButton: false,
    });
  } catch (err) {
    Swal.fire("Error", err.message, "error");
  }

  isSaving.value = false;
};
</script>

<style scoped>
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
  transition: 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 114, 255, 0.15);
}

/* Floating Labels */
.form-floating > label {
  padding-left: 12px;
}

.form-control {
  height: 48px;
  border-radius: 12px !important;
  border: 1.5px solid #d4d9e1;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.25s ease;
}

.form-control:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 0.15rem rgba(0, 114, 255, 0.15);
}

/* Title Gradient */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Gradient Button */
.btn-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  color: white;
  border: none;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 114, 255, 0.25);
}

/* Fade In */
.fade-in {
  animation: fadeIn 0.8s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
