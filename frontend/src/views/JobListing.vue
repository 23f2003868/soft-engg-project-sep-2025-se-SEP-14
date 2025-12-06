<template>
  <Navbar />

  <section class="job-listing-section py-5">
    <div class="container">
      <div class="text-center mb-5 fade-in">
        <h2 class="fw-bold text-primary mb-2">Available Job Listings</h2>
        <p class="text-muted fs-5">Find your next opportunity from top companies hiring today.</p>
      </div>

      <div class="row mb-4 fade-in">
        <div class="col-md-8 mx-auto">
          <div class="d-flex flex-column flex-md-row gap-3">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control rounded-4 shadow-sm"
              placeholder="Search job title, company, or location..."
            />
            <select v-model="selectedCategory" class="form-select rounded-4 shadow-sm">
              <option value="">All Job Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Internship">Internship</option>
              <option value="Remote">Remote</option>
              <option value="Contract">Contract</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="row g-4">
        <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
          <div class="job-card-skeleton glass-card p-4"></div>
        </div>
      </div>

      <div v-else>
        <div v-if="filteredJobs.length" class="row g-4 fade-in visible">
          <div
            v-for="job in visibleJobs"
            :key="job.job_id"
            class="col-md-6 col-lg-4"
          >
            <div class="job-card glass-card p-4 d-flex flex-column h-100">

              <div class="d-flex justify-content-between align-items-start mb-3">

                <div class="job-avatar">
                  <img :src="generateJobAvatar(job.job_title)" :alt="job.job_title + ' avatar'" />
                </div>

                <div class="flex-grow-1 ms-3">
                  <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>
                  <div class="small text-primary fw-semibold mb-1">
                    <i class="bi bi-building me-1"></i>
                    {{ job.company || "Confidential Company" }}
                  </div>
                  <div class="small text-muted">
                    <i class="bi bi-geo-alt me-1 text-primary"></i>{{ job.location }}
                  </div>
                </div>

                </div>

              <div class="small text-muted mb-1">
                <i class="bi bi-briefcase me-1 text-primary"></i>{{ job.job_type }}
              </div>

              <div class="small text-muted mb-1">
                <i class="bi bi-person-workspace me-1 text-primary"></i>
                Experience: <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
              </div>

              <div class="small text-muted mb-2">
                <i class="bi bi-calendar-event me-1 text-primary"></i>
                End Date: {{ formatReadableDate(job.end_date) }}
              </div>

              <p class="job-snippet text-secondary small mt-2 mb-3">
                {{ getShortDescription(job.description) }}
              </p>

              <div class="mb-3 d-flex flex-wrap gap-1">
                <span
                  v-for="skill in deriveJobSkills(job)"
                  :key="skill"
                  class="badge rounded-pill bg-light text-primary border small-pill"
                >
                  {{ skill }}
                </span>
              </div>

              <div class="d-flex justify-content-start gap-2 mt-auto">

                <button
                  class="btn btn-sm btn-outline-primary rounded-pill"
                  @click="openJobDetails(job)"
                >
                  View Details
                </button>
                
                <button
                  class="btn btn-sm btn-primary rounded-pill"
                  @click="onApplyClick(job)"
                >
                  Apply Now
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center text-muted mt-5 fade-in">
          <i class="bi bi-briefcase fs-1 text-secondary mb-3"></i>
          <p>No jobs match your filters.</p>
          <button class="btn btn-outline-primary rounded-pill btn-sm" @click="resetFilters">
            Reset filters
          </button>
        </div>

        <div v-if="visibleJobs.length < filteredJobs.length" class="d-flex justify-content-center mt-4">
          <button class="btn btn-outline-secondary rounded-pill btn-sm" @click="loadMore">
            Load more jobs
          </button>
        </div>
      </div>
    </div>
  </section>

  <div class="modal fade" id="jobDetailsModal" tabindex="-1" ref="jobDetailsModalRef">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content glass-modal border-0">

        <div class="modal-header border-0">
          <div>
            <h5 class="modal-title fw-bold">{{ selectedJob.job_title }}</h5>

            <p class="small text-muted mb-0">
              <i class="bi bi-geo-alt me-1 text-primary"></i>
              {{ selectedJob.location }}
              •
              <i class="bi bi-briefcase ms-2 me-1 text-primary"></i>
              {{ selectedJob.job_type }}
            </p>

            <p class="small text-muted">
              Experience: {{ formatExperience(selectedJob.experience) }}
              <span v-if="selectedJob.end_date"> | End Date: {{ formatReadableDate(selectedJob.end_date) }}</span>
            </p>
          </div>

          <button class="btn-close" data-bs-dismiss="modal" @click="closeJobDetails"></button>
        </div>

        <div class="modal-body">
          <hr />

          <h6 class="fw-semibold text-primary mb-2">Job Description</h6>
          <div class="small text-secondary markdown-body mb-3" v-html="jobDescriptionHtml"></div>

          <h6 class="fw-semibold text-primary mb-2">Skills</h6>
          <div class="mb-3 d-flex flex-wrap gap-1">
            <span
              v-for="skill in deriveJobSkills(selectedJob)"
              :key="skill"
              class="badge rounded-pill bg-light text-primary border small-pill"
            >
              {{ skill }}
            </span>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button
              class="btn btn-success btn-sm rounded-pill"
              @click="onApplyClick(selectedJob)"
            >
              Apply Now
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "../components/Navbar.vue";
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";


import publicApi from "../services/api.js"; 


const router = useRouter();

const jobs = ref([]);
const isLoading = ref(true);
const selectedJob = ref({}); // Holds job details for the modal

const allSkills = ref([
  "Python",
  "SQL",
  "VueJS",
  "JavaScript",
  "React",
  "Node.js",
  "Django",
  "Flask",
  "Machine Learning",
  "Data Analysis"
]);

// Filters
const searchQuery = ref("");
const selectedCategory = ref("");

// Pagination
const visibleCount = ref(9);
const jobsPerPage = 9;

// Refs for Modals
const jobDetailsModalRef = ref(null);
let jobDetailsModalInstance = null;


const categories = computed(() => {
    // Collect all unique job_type values for the filter dropdown
    // This is not used in the template anymore since we hardcoded the options, 
    // but kept here for consistency if needed later.
    return [...new Set(jobs.value.map((j) => j.job_type))].filter(Boolean);
});

const filteredJobs = computed(() => {
  let list = jobs.value.filter((job) => {
    // Search filter
    const searchString = `${job.job_title} ${job.company} ${job.location}`.toLowerCase();
    const matchesSearch = searchString.includes(searchQuery.value.toLowerCase());

    // Category filter (now relies on hardcoded select options)
    const matchesCategory =
      !selectedCategory.value || job.job_type === selectedCategory.value;

    return matchesSearch && matchesCategory;
  });
  
  return list;
});

const visibleJobs = computed(() => filteredJobs.value.slice(0, visibleCount.value));

const jobDescriptionHtml = computed(() =>
  selectedJob.value.description
    ? marked.parse(selectedJob.value.description)
    : "<p>No description available.</p>"
);


const fetchJobs = async () => {
    isLoading.value = true;
    try {
        // Use the publicApi instance that does NOT require a JWT token.
        const response = await publicApi.get("/api/jobs-all");
        
        if (response.data.success) {
            jobs.value = response.data.jobs || [];
        } else {
            console.error("API Error:", response.data.error || "Failed to fetch jobs.");
            jobs.value = [];
        }
        
    } catch (error) {
        console.error("Error fetching job listings:", error);
        // Show user-friendly alert on fetch failure
        Swal.fire({
            icon: 'error',
            title: 'Server Error',
            text: 'Failed to load job listings. Please check the backend server status.',
            confirmButtonText: 'OK',
        });
        jobs.value = [];

    } finally {
        isLoading.value = false;
        nextTick(initScrollReveal); // Trigger animations after data loads
    }
};


function formatExperience(exp) {
  const n = Number(exp);
  if (isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher";
  if (n === 1) return "1 year";
  return `${n} years`;
}

function formatReadableDate(raw) {
  if (!raw) return "Not specified";
  try {
      const d = new Date(raw);
      return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
  } catch {
      return raw;
  }
}

function getShortDescription(desc) {
  if (!desc) return "No description.";
  // Remove markdown formatting for a clean snippet
  let text = desc.replace(/[#*_`]/g, " ").replace(/\s+/g, " ").trim();
  return text.length <= 140 ? text : text.slice(0, 140) + "...";
}

function getInitialsFromTitle(title) {
  if (!title) return "JD";
  const parts = title.trim().split(" ");
  if (parts.length === 1) {
    return (parts[0][0] + (parts[0][1] || "D")).toUpperCase();
  }
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

function generateJobAvatar(title) {
  const initials = getInitialsFromTitle(title);
  // Using a consistent color scheme for avatars
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&background=3864f2&color=fff&rounded=true&size=52`;
}

function deriveJobSkills(job) {
    const txt = (job.description || "").toLowerCase();
    const detected = [];
    allSkills.value.forEach(skill => {
      if (txt.includes(skill.toLowerCase())) detected.push(skill);
    });
    return detected.length ? detected.slice(0, 4) : ["General"];
}

function loadMore() {
  visibleCount.value += jobsPerPage;
}

function resetFilters() {
    searchQuery.value = "";
    selectedCategory.value = "";
    visibleCount.value = jobsPerPage;
}

function openJobDetails(job) {
  selectedJob.value = { ...job };
  nextTick(() => jobDetailsModalInstance.show());
}

function closeJobDetails() {
  jobDetailsModalInstance.hide();
}

function onApplyClick(job) {
    // Check if the user is logged in by looking for the token
    const token = localStorage.getItem("token");

    if (!token) {
        // SCENARIO 1: UNAUTHENTICATED USER (Required Fix)
        Swal.fire({
            icon: 'info',
            title: 'Login Required',
            text: 'You must log in to start the application process.',
            showCancelButton: true,
            confirmButtonText: 'Go to Login',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                router.push("/login"); 
            }
        });
    } else {
        // SCENARIO 2: AUTHENTICATED USER (Check Role)
        const user = JSON.parse(localStorage.getItem('user'));
        const userRole = user ? user.role : null;

        if (userRole === 'CANDIDATE') {
            // Logged in as candidate, proceed to application/test page
            router.push(`/apply/${job.job_id}`);
        } else {
            // Logged in, but not as a candidate (e.g., Recruiter, Admin)
            Swal.fire({
                icon: 'error',
                title: 'Access Denied',
                text: 'Only Candidates are permitted to apply for jobs.',
                confirmButtonText: 'OK',
            });
        }
    }
}


const initScrollReveal = () => {
  const fadeEls = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );
  fadeEls.forEach((el) => observer.observe(el));
};

onMounted(() => {
    fetchJobs();

    // Initialize Bootstrap Modals
    if (jobDetailsModalRef.value) {
        jobDetailsModalInstance = new Modal(jobDetailsModalRef.value);
    }
});
</script>

<style scoped>

.job-listing-section {
    min-height: 100vh;
    background: radial-gradient(circle at top left, #e2ecff, #f4f7ff 45%, #e9f1ff 80%);
}

.fade-in {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

.glass-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  border: 1px solid rgba(207, 219, 240, 0.55);
  backdrop-filter: blur(14px);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.08);
  padding: 1.3rem 1.4rem;
}

.job-card {
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(220, 227, 240, 0.65);
  backdrop-filter: blur(14px);
  transition: 0.28s ease;
  padding: 1.6rem !important;
  display: flex;
  flex-direction: column;
}

.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 22px 46px rgba(25, 40, 70, 0.22);
}

/* Avatar */
.job-avatar {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  overflow: hidden;
  background: #eef6ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.job-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.job-snippet {
  font-size: 0.88rem;
  line-height: 1.45;
  color: #4a5568;
}

.job-card-skeleton {
  border-radius: 1.5rem;
  padding: 1.5rem;
  background: #fff;
  height: 350px;
  /* Simplified skeleton visual, needs actual CSS/keyframes if using shimmer */
  background: linear-gradient(90deg, #edf2ff 0%, #dfe7f3 50%, #edf2ff 100%);
}

.glass-modal {
  background: rgba(255, 255, 255, 0.96);
  border-radius: 1.4rem;
  backdrop-filter: blur(20px);
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}
.modal-body::-webkit-scrollbar-thumb {
  background: #c7d4ff;
  border-radius: 10px;
}

.markdown-body {
  font-size: 0.92rem;
  line-height: 1.55;
  /* Ensure markdown rendering is clean */
  white-space: pre-wrap;
}

.small-pill {
    font-size: 0.75rem;
    padding: 0.3em 0.8em;
}
</style>