<template>
  <Navbar />

  <section class="profile-section py-5">
    <div class="container">
      <div class="text-center mb-4 fade-in">
        <h2 class="fw-bold text-gradient">Recruiter Profile</h2>
        <p class="text-muted">Update your company details</p>
      </div>

      <div class="profile-card shadow-lg p-4 p-md-5 fade-in">

        <form @submit.prevent="saveProfile">

          <!-- FIRST NAME -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.firstname" type="text" class="form-control" placeholder="First Name" required />
            <label>First Name</label>
          </div>

          <!-- LAST NAME -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.lastname" type="text" class="form-control" placeholder="Last Name" required />
            <label>Last Name</label>
          </div>

          <!-- EMAIL -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.email" type="email" class="form-control" placeholder="Email" required />
            <label>Email</label>
          </div>

          <!-- COMPANY -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.company" type="text" class="form-control" placeholder="Company Name" required />
            <label>Company Name</label>
          </div>

          <!-- POSITION -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.position" type="text" class="form-control" placeholder="Position" required />
            <label>Position</label>
          </div>

          <!-- LINKEDIN -->
          <div class="form-floating mb-3">
            <input v-model.trim="profile.linkedin" type="url" class="form-control" placeholder="LinkedIn Profile" />
            <label>LinkedIn Profile</label>
          </div>

          <!-- BUTTON -->
          <div class="text-end mt-4">
            <button type="submit" class="btn btn-gradient rounded-3 shadow-sm px-4" :disabled="isSaving">
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
import Navbar from '../components/RecruiterNavbar.vue';
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';

const API_URL = "http://127.0.0.1:5000";
const token = localStorage.getItem("token");

const profile = ref({
  firstname: "",
  lastname: "",
  email: "",
  company: "",
  position: "",
  linkedin: ""
});

const isSaving = ref(false);

onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/api/index`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();
    if (!data.success) return;

    const user = data.user;

    profile.value.firstname = user.firstname;
    profile.value.lastname = user.lastname;
    profile.value.email = user.email;
    profile.value.company = user.recruiter.company;
    profile.value.position = user.recruiter.position;
    profile.value.linkedin = user.recruiter.linkdin_profile_path;

  } catch (err) {
    console.error("Profile fetch failed:", err);
  }
});

const saveProfile = async () => {

  if (!profile.value.firstname || !profile.value.lastname || !profile.value.email || !profile.value.company || !profile.value.position) {
    Swal.fire({
      icon: "warning",
      title: "Missing Information",
      text: "Please fill all required fields."
    });
    return;
  }

  isSaving.value = true;

  const body = {
    firstname: profile.value.firstname,
    lastname: profile.value.lastname,
    email: profile.value.email,
    company: profile.value.company,
    position: profile.value.position,
    linkdin_profile_path: profile.value.linkedin
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
      Swal.fire({ icon: "error", title: "Update Failed", text: data.error });
      return;
    }

    Swal.fire({
      icon: "success",
      title: "Profile Updated",
      text: "Your profile has been successfully updated!",
      timer: 1800,
      showConfirmButton: false
    });

  } catch (error) {
    Swal.fire({ icon: "error", title: "Error", text: error.message });
  }

  isSaving.value = false;
};
</script>

<style scoped>
.profile-section {
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
  min-height: calc(100vh - 80px);
}

/* Premium Card */
.profile-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);
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
  height: 48px !important;
  border-radius: 12px !important;
  border: 1.5px solid #d4d9e1;
  transition: all 0.2s ease-in-out;
}

.form-control:focus {
  border-color: #0b5ed7;
  box-shadow: 0 0 0 0.15rem rgba(11, 94, 215, 0.25);
}

/* Gradient Title */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  color: transparent;
}

/* Save Button */
.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff;
  transition: all 0.3s ease;
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
