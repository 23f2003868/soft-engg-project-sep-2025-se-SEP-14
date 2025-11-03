<template>
  <Navbar />

  <section class="profile-section py-5">
    <div class="container">
      <div class="text-center mb-4 fade-in">
        <h2 class="fw-bold text-primary">Recruiter Profile</h2>
        <p class="text-muted">Update your company and role details</p>
      </div>

      <div class="bg-white p-4 rounded-4 shadow-sm fade-in">
        <form @submit.prevent="saveProfile">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input
              v-model.trim="profile.name"
              type="text"
              class="form-control"
              placeholder="Enter your full name"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model.trim="profile.email"
              type="email"
              class="form-control"
              placeholder="Enter your email"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Company Name</label>
            <input
              v-model.trim="profile.company"
              type="text"
              class="form-control"
              placeholder="Enter your company name"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Position</label>
            <input
              v-model.trim="profile.position"
              type="text"
              class="form-control"
              placeholder="Enter your job position"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">LinkedIn Profile</label>
            <input
              v-model.trim="profile.linkedin"
              type="url"
              class="form-control"
              placeholder="https://linkedin.com/in/username"
            />
          </div>

          <div class="text-end mt-4">
            <button
              type="submit"
              class="btn btn-primary rounded-3 shadow-sm"
              :disabled="isSaving"
            >
              <i v-if="isSaving" class="bi bi-hourglass-split me-2"></i>
              <i v-else class="bi bi-save me-2"></i>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
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

// Recruiter profile data
const profile = ref({
  name: '',
  email: '',
  company: '',
  position: '',
  linkedin: '',
});

// Simulated loading state
const isSaving = ref(false);

// Dummy data prefill
onMounted(() => {
  profile.value = {
    name: 'Riya Sharma',
    email: 'riya.sharma@technova.in',
    company: 'TechNova Pvt. Ltd.',
    position: 'HR Manager',
    linkedin: 'https://linkedin.com/in/riyasharma',
  };
});

// Save function with validation and error handling
const saveProfile = async () => {
  try {
    // Simple validation
    if (
      !profile.value.name ||
      !profile.value.email ||
      !profile.value.company ||
      !profile.value.position
    ) {
      Swal.fire({
        icon: 'warning',
        title: 'Incomplete Information',
        text: 'Please fill out all required fields before saving.',
      });
      return;
    }

    isSaving.value = true;

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Simulate saving in localStorage
    localStorage.setItem('recruiterProfile', JSON.stringify(profile.value));

    Swal.fire({
      icon: 'success',
      title: 'Profile Updated',
      text: 'Recruiter profile saved successfully!',
      timer: 2000,
      showConfirmButton: false,
    });
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Something went wrong!',
      text: error.message || 'Failed to save your profile. Please try again later.',
    });
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.profile-section {
  background-color: #f8f9fa;
}
.form-label {
  font-weight: 600;
}
.fade-in {
  animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
button {
  transition: 0.3s;
}
button:hover {
  transform: translateY(-2px);
}
</style>
