<template>
  <Navbar />

  <section class="profile-section py-5">
    <div class="container">

      <!-- Header -->
      <div class="text-center mb-4 fade-in">
        <h2 class="fw-bold text-gradient">Recruiter Profile</h2>
        <p class="text-muted">Manage your recruitment identity and company details</p>
      </div>

      <!-- CARD -->
      <div class="profile-card shadow-lg p-4 p-md-5 fade-in">

        <form @submit.prevent="saveProfile">

          <!-- FIRST NAME -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.firstname"
              type="text"
              class="form-control"
              placeholder="First Name"
              required
            />
            <label>First Name</label>
          </div>

          <!-- LAST NAME -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.lastname"
              type="text"
              class="form-control"
              placeholder="Last Name"
              required
            />
            <label>Last Name</label>
          </div>

          <!-- EMAIL -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.email"
              type="email"
              class="form-control"
              placeholder="Email"
              required
            />
            <label>Email</label>
          </div>

          <!-- COMPANY -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.company"
              type="text"
              class="form-control"
              placeholder="Company Name"
              required
            />
            <label>Company Name</label>
          </div>

          <!-- POSITION -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.position"
              type="text"
              class="form-control"
              placeholder="Position"
              required
            />
            <label>Position</label>
          </div>

          <!-- LINKEDIN -->
          <div class="form-floating mb-3">
            <input
              v-model.trim="profile.linkedin"
              type="url"
              class="form-control"
              placeholder="LinkedIn Profile URL"
            />
            <label>LinkedIn Profile</label>
          </div>

          <!-- COMPANY ABOUT -->
          <div class="mb-3">
            <label class="form-label fw-semibold">About Company</label>
            <textarea
              v-model.trim="profile.company_about"
              class="form-control"
              rows="5"
              placeholder="Write about your company…"
            ></textarea>
          </div>

          <!-- Save Button -->
          <div class="text-end mt-4">
            <button
              type="submit"
              class="btn btn-gradient rounded-3 shadow-sm px-4"
              :disabled="isSaving"
            >
              <span v-if="isSaving">
                <i class="bi bi-hourglass-split me-2"></i>Saving…
              </span>
              <span v-else>
                <i class="bi bi-save me-2"></i>Save Changes
              </span>
            </button>
          </div>

        </form>

      </div>
    </div>
  </section>
</template>

<script setup>
import Navbar from "../components/RecruiterNavbar.vue";
import { ref, onMounted } from "vue";
import Swal from "sweetalert2";

const API_URL = "http://127.0.0.1:5000";
const token = localStorage.getItem("token");

const profile = ref({
  firstname: "",
  lastname: "",
  email: "",
  company: "",
  position: "",
  linkedin: "",
  company_about: ""
});

const isSaving = ref(false);

// Load recruiter details
onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/api/index`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();
    if (!data.success) return;

    const user = data.user;
    const rec = user.recruiter;

    profile.value.firstname = user.firstname;
    profile.value.lastname = user.lastname;
    profile.value.email = user.email;

    profile.value.company = rec.company;
    profile.value.position = rec.position;
    profile.value.linkedin = rec.linkdin_profile_path || "";
    profile.value.company_about = rec.company_about || "";

  } catch (err) {
    console.error("Failed loading profile:", err);
  }
});

// Save recruiter profile
const saveProfile = async () => {
  const b = profile.value;

  if (!b.firstname || !b.lastname || !b.email || !b.company || !b.position) {
    return Swal.fire({
      icon: "warning",
      title: "Missing Details",
      text: "Please fill all required fields."
    });
  }

  isSaving.value = true;

  const body = {
    firstname: b.firstname,
    lastname: b.lastname,
    email: b.email,
    company: b.company,
    position: b.position,
    company_about: b.company_about,
    linkdin_profile_path: b.linkedin
  };

  try {
    const res = await fetch(`${API_URL}/api/update-recruiter`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    const data = await res.json();

    if (!res.ok) {
      return Swal.fire({
        icon: "error",
        title: "Error Updating",
        text: data.error || data.message
      });
    }

    Swal.fire({
      icon: "success",
      title: "Updated Successfully",
      text: "Your profile has been updated!",
      timer: 1500,
      showConfirmButton: false
    });

  } catch (err) {
    Swal.fire({ icon: "error", title: "Network Error", text: err.message });
  }

  isSaving.value = false;
};
</script>

<style scoped>
.profile-section {
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
  min-height: calc(100vh - 80px);
}

/* Glassmorphic Card */
.profile-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: 0.3s ease;
}
.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(0, 114, 255, 0.15);
}

/* Floating Labels */
.form-floating > label {
  padding-left: 14px;
}
.form-control {
  height: 48px !important;
  border-radius: 12px !important;
  border: 1.5px solid #d4d9e1;
}
.form-control:focus {
  border-color: #0b5ed7;
  box-shadow: 0 0 0 0.15rem rgba(11, 94, 215, 0.25);
}

/* Gradient Headings */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  color: transparent;
}

/* Button */
.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff;
  transition: 0.3s ease;
}
.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 114, 255, 0.25);
}

/* Animation */
.fade-in {
  animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
