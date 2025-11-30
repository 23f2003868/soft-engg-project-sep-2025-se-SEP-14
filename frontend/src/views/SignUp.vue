<template>
  <Navbar />

  <div class="signup-container d-flex justify-content-center align-items-center py-5">
    <div class="signup-card shadow-lg p-4 p-md-5">
      <div class="card-body">

        <h2 class="text-center fw-bold text-gradient mb-3">Create Account 🚀</h2>
        <p class="text-center text-muted mb-4">
          Join <span class="fw-semibold">ApplAI</span> and start your dream career today.
        </p>

        <form @submit.prevent="handleSignup" novalidate>

          <!-- ROLE -->
          <div class="form-floating mb-3">
            <select v-model="role" 
              class="form-select rounded-3 shadow-sm"
              :class="{ 'is-invalid': roleError }">
              <option value="">Select Role</option>
              <option value="CANDIDATE">Candidate</option>
              <option value="RECRUITER">Recruiter</option>
            </select>
            <label>Register As</label>
            <div class="invalid-feedback small">{{ roleError }}</div>
          </div>

          <!-- FIRST NAME -->
          <div class="form-floating mb-3">
            <input type="text" v-model="firstname"
              placeholder="First Name"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': firstnameError }" />
            <label>First Name</label>
            <div class="invalid-feedback small">{{ firstnameError }}</div>
          </div>

          <!-- LAST NAME -->
          <div class="form-floating mb-3">
            <input type="text" v-model="lastname"
              placeholder="Last Name"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': lastnameError }" />
            <label>Last Name</label>
            <div class="invalid-feedback small">{{ lastnameError }}</div>
          </div>

          <!-- EMAIL -->
          <div class="form-floating mb-3">
            <input type="email" v-model="email"
              placeholder="name@example.com"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': emailError }" />
            <label>Email Address</label>
            <div class="invalid-feedback small">{{ emailError }}</div>
          </div>

          <!-- PASSWORD -->
          <div class="form-floating mb-3">
            <input type="password" v-model="password"
              placeholder="Password"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': passwordError }" />
            <label>Password</label>
            <div class="invalid-feedback small">{{ passwordError }}</div>
          </div>

          <!-- CONFIRM PASSWORD -->
          <div class="form-floating mb-4">
            <input type="password" v-model="confirmPassword"
              placeholder="Confirm Password"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': confirmPasswordError }" />
            <label>Confirm Password</label>
            <div class="invalid-feedback small">{{ confirmPasswordError }}</div>
          </div>

          <!-- Candidate Fields -->
          <template v-if="role === 'CANDIDATE'">

            <div class="form-floating mb-3">
              <input type="number" v-model="age"
                placeholder="Age"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': ageError }" />
              <label>Age</label>
              <div class="invalid-feedback small">{{ ageError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input type="text" v-model="education"
                placeholder="Education"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': educationError }" />
              <label>Education</label>
              <div class="invalid-feedback small">{{ educationError }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Upload Resume</label>
              <input type="file" @change="handleFile"
                class="form-control shadow-sm rounded-3"
                :class="{ 'is-invalid': resumeError }" />
              <div class="invalid-feedback small">{{ resumeError }}</div>
            </div>

          </template>

          <!-- Recruiter Fields -->
          <template v-if="role === 'RECRUITER'">

            <div class="form-floating mb-3">
              <input type="text" v-model="company"
                placeholder="Company"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': companyError }" />
              <label>Company</label>
              <div class="invalid-feedback small">{{ companyError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input type="text" v-model="position"
                placeholder="Position"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': positionError }" />
              <label>Position</label>
              <div class="invalid-feedback small">{{ positionError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input type="url" v-model="linkdin"
                placeholder="https://linkedin.com/in/username"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': linkdinError }" />
              <label>LinkedIn Profile</label>
              <div class="invalid-feedback small">{{ linkdinError }}</div>
            </div>

          </template>

          <!-- Server Error -->
          <div v-if="serverError" class="alert alert-danger text-center small py-2 mb-3">
            {{ serverError }}
          </div>

          <!-- SUBMIT BUTTON -->
          <button type="submit"
            class="btn btn-gradient w-100 fw-bold py-2 rounded-3 shadow-sm"
            :disabled="isLoading">
            {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
          </button>

        </form>

        <p class="text-center mt-4 small text-muted">
          Already have an account?
          <router-link to="/login" class="fw-semibold text-gradient text-decoration-none">
            Log In
          </router-link>
        </p>

      </div>
    </div>
  </div>
</template>


<script setup>
import Navbar from '../components/Navbar.vue';
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const router = useRouter();
const API_URL = "http://127.0.0.1:5000";

// 🔹 Shared LinkedIn regex (used in validate + watchers)
const linkedinRegex = /^https:\/\/(www\.)?linkedin\.com\/.*$/;

const role = ref("");
const firstname = ref("");
const lastname = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const age = ref("");
const education = ref("");
const resumeFile = ref(null);

const company = ref("");
const position = ref("");
const linkdin = ref("");

const roleError = ref("");
const firstnameError = ref("");
const lastnameError = ref("");
const emailError = ref("");
const passwordError = ref("");
const confirmPasswordError = ref("");
const ageError = ref("");
const educationError = ref("");
const resumeError = ref("");
const companyError = ref("");
const positionError = ref("");
const linkdinError = ref("");
const serverError = ref("");

const isLoading = ref(false);

const handleFile = (e) => resumeFile.value = e.target.files[0];

/* 🔥 LIVE ERROR CLEARING WHEN USER FIXES INPUT */
watch(role, (val) => {
  if (val) roleError.value = "";
});

watch(firstname, (val) => {
  if (val) firstnameError.value = "";
});

watch(lastname, (val) => {
  if (val) lastnameError.value = "";
});

watch(email, (val) => {
  if (val && val.includes("@")) emailError.value = "";
});

watch(password, (val) => {
  if (val && val.length >= 6) passwordError.value = "";
  // also re-check confirmPassword match
  if (confirmPassword.value && val === confirmPassword.value) {
    confirmPasswordError.value = "";
  }
});

watch(confirmPassword, (val) => {
  if (val && val === password.value) confirmPasswordError.value = "";
});

watch(age, (val) => {
  if (val) ageError.value = "";
});

watch(education, (val) => {
  if (val) educationError.value = "";
});

watch(resumeFile, (val) => {
  if (val) resumeError.value = "";
});

watch(company, (val) => {
  if (val) companyError.value = "";
});

watch(position, (val) => {
  if (val) positionError.value = "";
});

watch(linkdin, (val) => {
  if (val && linkedinRegex.test(val.trim())) {
    linkdinError.value = "";
  }
});

const validateForm = () => {
  let valid = true;

  if (!role.value) { roleError.value = "Please select role"; valid = false; }
  if (!firstname.value) { firstnameError.value = "First name required"; valid = false; }
  if (!lastname.value) { lastnameError.value = "Last name required"; valid = false; }
  if (!email.value.includes("@")) { emailError.value = "Invalid email"; valid = false; }
  if (password.value.length < 6) { passwordError.value = "Min 6 characters"; valid = false; }
  if (password.value !== confirmPassword.value) { confirmPasswordError.value = "Passwords do not match"; valid = false; }

  if (role.value === "CANDIDATE") {
    if (!age.value) { ageError.value = "Age required"; valid = false; }
    if (!education.value) { educationError.value = "Education required"; valid = false; }
    if (!resumeFile.value) { resumeError.value = "Resume required"; valid = false; }
  }

  if (role.value === "RECRUITER") {
    if (!company.value) { companyError.value = "Company required"; valid = false; }
    if (!position.value) { positionError.value = "Position required"; valid = false; }

    if (!linkdin.value) {
      linkdinError.value = "LinkedIn link required";
      valid = false;
    } else if (!linkedinRegex.test(linkdin.value.trim())) {
      linkdinError.value = "Enter a valid LinkedIn URL (example: https://www.linkedin.com/in/username)";
      valid = false;
    }
  }

  return valid;
};

const handleSignup = async () => {
  serverError.value = "";

  if (!validateForm()) return;

  isLoading.value = true;

  try {
    if (role.value === "CANDIDATE") {
      let formData = new FormData();
      formData.append("file", resumeFile.value);

      const userData = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
        password: password.value,
        age: age.value,
        education: education.value,
      };

      formData.append("user_data", JSON.stringify(userData));

      const res = await fetch(`${API_URL}/api/register-candidate`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || data.message || "Signup failed");
    }

    if (role.value === "RECRUITER") {
      let body = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
        password: password.value,
        company: company.value,
        position: position.value,
        linkdin_profile_path: linkdin.value,
      };

      const res = await fetch(`${API_URL}/api/register-recruiter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || data.message || "Signup failed");
    }

    Swal.fire({
      icon: "success",
      title: "Account created!",
      text: "You can now log in.",
      timer: 2000,
      showConfirmButton: false,
    });

    router.push("/login?signupSuccess=true");
  } catch (err) {
    serverError.value = err.message;
  }

  isLoading.value = false;
};
</script>

<style scoped>
.signup-container {
  min-height: calc(100vh - 80px);
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
  backdrop-filter: blur(10px);
}

/* Glassmorphism Card */
.signup-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  max-width: 460px;
  width: 100%;
  transition: 0.3s ease;
}

.signup-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 114, 255, 0.15);
}

/* Floating Labels Premium Style */
.form-floating > label {
  padding-left: 12px;
}

.form-control,
.form-select {
  height: 48px !important;
  font-size: 15px;
  border-radius: 12px !important;
  border: 1.5px solid #d4d9e1;
  transition: all 0.2s ease-in-out;
}

.form-control:focus,
.form-select:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 0.15rem rgba(0, 114, 255, 0.15);
}

/* Gradient Title */
.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  color: transparent;
}

/* Gradient Button */
.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: white;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 114, 255, 0.25);
}
</style>
