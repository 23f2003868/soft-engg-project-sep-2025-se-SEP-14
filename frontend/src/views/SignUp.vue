<template>
  <Navbar />

  <div class="signup-container d-flex justify-content-center align-items-center py-5">
    <div class="signup-card shadow-lg p-4 p-md-5">
      <div class="card-body">

        <h2 class="text-center fw-bold text-gradient mb-3">Create Account 🚀</h2>
        <p class="text-center text-muted mb-4">
          Join <span class="fw-semibold">ApplAI</span> and unlock smart career opportunities.
        </p>

        <form @submit.prevent="handleSignup" novalidate>

          <!-- ROLE -->
          <div class="form-floating mb-3">
            <select 
              v-model="role"
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
            <input 
              type="text" v-model="firstname"
              placeholder="Enter your first name"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': firstnameError }"
            />
            <label>First Name</label>
            <div class="invalid-feedback small">{{ firstnameError }}</div>
          </div>

          <!-- LAST NAME -->
          <div class="form-floating mb-3">
            <input 
              type="text" v-model="lastname"
              placeholder="Enter your last name"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': lastnameError }"
            />
            <label>Last Name</label>
            <div class="invalid-feedback small">{{ lastnameError }}</div>
          </div>

          <!-- EMAIL -->
          <div class="form-floating mb-3">
            <input 
              type="email" v-model="email"
              placeholder="name@example.com"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': emailError }"
            />
            <label>Email Address</label>
            <div class="invalid-feedback small">{{ emailError }}</div>
          </div>

          <!-- PASSWORD -->
          <div class="form-floating mb-3">
            <input 
              type="password" v-model="password"
              placeholder="Minimum 6 characters"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': passwordError }"
            />
            <label>Password</label>
            <div class="invalid-feedback small">{{ passwordError }}</div>
          </div>

          <!-- CONFIRM PASSWORD -->
          <div class="form-floating mb-4">
            <input 
              type="password" v-model="confirmPassword"
              placeholder="Re-enter your password"
              class="form-control rounded-3 shadow-sm"
              :class="{ 'is-invalid': confirmPasswordError }"
            />
            <label>Confirm Password</label>
            <div class="invalid-feedback small">{{ confirmPasswordError }}</div>
          </div>

          <!-- ========================= -->
          <!-- CANDIDATE FIELDS -->
          <!-- ========================= -->
          <template v-if="role === 'CANDIDATE'">

            <div class="form-floating mb-3">
              <input 
                type="number" v-model="age"
                placeholder="Enter your age"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': ageError }"
              />
              <label>Age</label>
              <div class="invalid-feedback small">{{ ageError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input 
                type="text" v-model="education"
                placeholder="Your qualification"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': educationError }"
              />
              <label>Education</label>
              <div class="invalid-feedback small">{{ educationError }}</div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Upload Resume</label>
              <input 
                type="file" @change="handleFile"
                class="form-control shadow-sm rounded-3"
                :class="{ 'is-invalid': resumeError }"
              />
              <div class="invalid-feedback small">{{ resumeError }}</div>
            </div>

          </template>

          <!-- ========================= -->
          <!-- RECRUITER FIELDS -->
          <!-- ========================= -->
          <template v-if="role === 'RECRUITER'">

            <div class="form-floating mb-3">
              <input 
                type="text" v-model="company"
                placeholder="Company name"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': companyError }"
              />
              <label>Company</label>
              <div class="invalid-feedback small">{{ companyError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input 
                type="text" v-model="position"
                placeholder="Recruiter position"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': positionError }"
              />
              <label>Position</label>
              <div class="invalid-feedback small">{{ positionError }}</div>
            </div>

            <!-- new field as required by backend -->
            <div class="form-floating mb-3">
              <textarea 
                v-model="company_about"
                placeholder="Describe your company in 2–4 lines"
                class="form-control rounded-3 shadow-sm"
                style="height: 100px;"
                :class="{ 'is-invalid': companyAboutError }"
              ></textarea>
              <label>About Company</label>
              <div class="invalid-feedback small">{{ companyAboutError }}</div>
            </div>

            <div class="form-floating mb-3">
              <input 
                type="url" v-model="linkdin"
                placeholder="https://www.linkedin.com/in/your-profile"
                class="form-control rounded-3 shadow-sm"
                :class="{ 'is-invalid': linkdinError }"
              />
              <label>LinkedIn Profile</label>
              <div class="invalid-feedback small">{{ linkdinError }}</div>
            </div>

          </template>

          <!-- SERVER ERROR -->
          <div v-if="serverError" class="alert alert-danger text-center small py-2 mb-3">
            {{ serverError }}
          </div>

          <!-- SUBMIT BUTTON -->
          <button 
            type="submit"
            class="btn btn-gradient w-100 fw-bold py-2 rounded-3 shadow-sm"
            :disabled="isLoading"
          >
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

// LinkedIn validation pattern
const linkedinRegex = /^https:\/\/(www\.)?linkedin\.com\/(in|company)\/[A-Za-z0-9_\-]+\/?$/;

// Form fields
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
const company_about = ref("");
const linkdin = ref("");

// Error fields
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
const companyAboutError = ref("");
const linkdinError = ref("");
const serverError = ref("");

const isLoading = ref(false);

const handleFile = (e) => {
  resumeFile.value = e.target.files[0];
  resumeError.value = "";
};

// Live error clearing
const clear = (v, r) => { if (v) r.value = ""; };

watch(role, (v) => clear(v, roleError));
watch(firstname, (v) => clear(v.trim(), firstnameError));
watch(lastname, (v) => clear(v.trim(), lastnameError));
watch(email, (v) => { if (v.includes("@")) emailError.value = ""; });
watch(password, (v) => {
  if (v.length >= 6) passwordError.value = "";
  if (confirmPassword.value && v === confirmPassword.value)
    confirmPasswordError.value = "";
});
watch(confirmPassword, (v) => {
  if (v === password.value) confirmPasswordError.value = "";
});
watch(age, (v) => clear(v, ageError));
watch(education, (v) => clear(v.trim(), educationError));
watch(company, (v) => clear(v.trim(), companyError));
watch(position, (v) => clear(v.trim(), positionError));
watch(company_about, (v) => clear(v.trim(), companyAboutError));
watch(linkdin, (v) => {
  if (linkedinRegex.test(v.trim())) linkdinError.value = "";
});

// VALIDATION
const validateForm = () => {
  let valid = true;

  if (!role.value) { roleError.value = "Select role"; valid = false; }

  if (!firstname.value.trim()) { firstnameError.value = "First name required"; valid = false; }
  if (!lastname.value.trim()) { lastnameError.value = "Last name required"; valid = false; }

  if (!email.value.includes("@")) { emailError.value = "Invalid email"; valid = false; }

  if (password.value.length < 6) { passwordError.value = "Min 6 characters"; valid = false; }

  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = "Passwords do not match";
    valid = false;
  }

  // Candidate
  if (role.value === "CANDIDATE") {
    if (!age.value || age.value < 16) { ageError.value = "Enter valid age"; valid = false; }
    if (!education.value.trim()) { educationError.value = "Education required"; valid = false; }
    if (!resumeFile.value) { resumeError.value = "Resume required"; valid = false; }
  }

  // Recruiter
  if (role.value === "RECRUITER") {
    if (!company.value.trim()) { companyError.value = "Company name required"; valid = false; }
    if (!position.value.trim()) { positionError.value = "Position required"; valid = false; }

    if (!company_about.value.trim()) {
      companyAboutError.value = "Company about required";
      valid = false;
    }

    if (!linkdin.value.trim()) {
      linkdinError.value = "LinkedIn required";
      valid = false;
    } else if (!linkedinRegex.test(linkdin.value.trim())) {
      linkdinError.value = "Invalid LinkedIn URL";
      valid = false;
    }
  }

  return valid;
};

// HANDLE SIGNUP
const handleSignup = async () => {
  serverError.value = "";

  if (!validateForm()) return;

  isLoading.value = true;

  try {
    // CANDIDATE
    if (role.value === "CANDIDATE") {
      const formData = new FormData();
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

      const res = await fetch(`${API_URL}/api/register-candidate`, {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.message || "Signup failed");
    }

    // RECRUITER
    if (role.value === "RECRUITER") {
      const body = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
        password: password.value,
        company: company.value,
        position: position.value,
        linkdin_profile_path: linkdin.value,
        company_about: company_about.value,
      };

      const res = await fetch(`${API_URL}/api/register-recruiter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.message);
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

.signup-card {
  background: rgba(255, 255, 255, 0.88);
  border-radius: 1.25rem;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.45);
  max-width: 480px;
  width: 100%;
}

.text-gradient {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  color: transparent;
}

.btn-gradient {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: white;
  transition: 0.3s;
}
.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 114, 255, 0.25);
}
</style>
