<template>
  <div class="saved-jobs-page">
    <CandidateNavbar />

    <section class="saved-section py-4 py-md-5">
      <div class="container">

        <!-- PAGE HEADER -->
        <div class="mb-4 fade-in visible">
          <h3 class="fw-bold text-primary mb-1">Saved Jobs</h3>
          <p class="text-muted small mb-0">
            Jobs you saved for later review & application.
          </p>
        </div>

        <!-- JOB GRID -->
        <div v-if="loading" class="row g-4 mt-2">
          <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
            <div class="job-card-skeleton glass-card p-4"></div>
          </div>
        </div>

        <div v-else>
          <div v-if="savedJobs.length" class="row g-4 fade-in visible">

            <div
              v-for="job in savedJobs"
              :key="job.job_id"
              class="col-md-6 col-lg-4"
            >
              <div class="job-card glass-card p-4 h-100 d-flex flex-column">

                <!-- Job header -->
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>
                    <div class="small text-muted">
                      <i class="bi bi-geo-alt me-1 text-primary"></i>
                      {{ job.location || "Not specified" }}
                    </div>
                  </div>

                  <!-- Unsave -->
                  <button
                    class="btn btn-sm rounded-circle favorite-btn favorite-btn-active"
                    @click="unsaveJob(job)"
                    title="Unsave job"
                  >
                    <i class="bi bi-bookmark-fill"></i>
                  </button>
                </div>

                <!-- Meta -->
                <div class="small text-muted mb-1">
                  <i class="bi bi-briefcase me-1 text-primary"></i>
                  {{ job.job_type }}
                </div>

                <div class="small text-muted mb-1">
                  <i class="bi bi-person-workspace me-1 text-primary"></i>
                  Experience:
                  <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
                </div>

                <div class="small text-muted mb-2">
                  <i class="bi bi-calendar-event me-1 text-primary"></i>
                  End Date:
                  <span class="fw-semibold">{{ formatReadableDate(job.end_date) }}</span>
                </div>

                <!-- Snippet -->
                <p class="job-snippet text-secondary small flex-grow-1">
                  {{ getShortDescription(job.description) }}
                </p>

                <!-- Skills -->
                <div class="mb-3 d-flex flex-wrap gap-1">
                  <span
                    v-for="skill in deriveJobSkills(job)"
                    :key="skill"
                    class="badge rounded-pill bg-light text-primary border small-pill"
                  >
                    {{ skill }}
                  </span>
                </div>

                <!-- Actions -->
                <div class="d-flex justify-content-between align-items-center mt-2">
                  <button
                    class="btn btn-sm btn-outline-primary rounded-pill"
                    @click="openJobModal(job)"
                    data-bs-toggle="modal"
                    data-bs-target="#savedJobModal"
                  >
                    View Details
                  </button>

                  <button
                    class="btn btn-sm btn-success rounded-pill"
                    @click="openApplyComingSoon(job)"
                  >
                    Apply
                  </button>
                </div>

              </div>
            </div>

          </div>

          <div v-else class="text-center text-muted mt-5 fade-in visible">
            <i class="bi bi-bookmark fs-1 text-secondary d-block mb-3"></i>
            <p class="mb-1">You haven't saved any jobs yet.</p>
            <p class="small">Go explore opportunities and save the ones you like!</p>
          </div>
        </div>

      </div>
    </section>

    <!-- MODAL: FULL DESCRIPTION -->
    <div
      class="modal fade"
      id="savedJobModal"
      tabindex="-1"
      aria-hidden="true"
      ref="savedJobModalRef"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header border-0">
            <div>
              <h5 class="modal-title fw-bold">
                {{ selectedJob?.job_title }}
              </h5>

              <p class="small text-muted mb-0">
                <i class="bi bi-geo-alt me-1 text-primary"></i>
                {{ selectedJob?.location }}
              </p>

              <p class="small text-muted mb-0">
                <i class="bi bi-person-workspace me-1 text-primary"></i>
                Experience:
                <span class="fw-semibold">
                  {{ formatExperience(selectedJob?.experience) }}
                </span>
              </p>

              <p class="small text-muted mb-0">
                <i class="bi bi-calendar-event me-1 text-primary"></i>
                End Date:
                <span class="fw-semibold">
                  {{ formatReadableDate(selectedJob?.end_date) }}
                </span>
              </p>
            </div>

            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body pt-0">
            <hr />
            <h6 class="fw-semibold text-primary">Job Description</h6>
            <div v-html="jobMarkdownHtml" class="small text-secondary markdown-body"></div>

            <h6 class="fw-semibold text-primary mt-3">Skills</h6>
            <div class="d-flex flex-wrap gap-1">
              <span
                v-for="skill in deriveJobSkills(selectedJob || {})"
                :key="skill"
                class="badge rounded-pill bg-light text-primary border small-pill"
              >
                {{ skill }}
              </span>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-3">
              <button
                class="btn btn-outline-primary btn-sm rounded-pill"
                @click="unsaveJob(selectedJob)"
              >
                <i class="bi bi-bookmark-dash me-1"></i> Unsave
              </button>

              <button
                class="btn btn-success btn-sm rounded-pill"
                @click="openApplyComingSoon(selectedJob)"
              >
                Apply
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- APPLY COMING SOON MODAL -->
    <div
      class="modal fade"
      id="applyComingSoonModal"
      tabindex="-1"
      aria-hidden="true"
      ref="applyModalRef"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header">
            <h5 class="modal-title fw-bold">Application Coming Soon</h5>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <p class="small text-muted mb-1">You selected:</p>
            <p class="fw-semibold">{{ jobForApply?.job_title }}</p>
            <p class="small text-secondary mb-0">
              Application flow will open soon. Stay tuned!
            </p>
          </div>

          <div class="modal-footer border-0">
            <button class="btn btn-sm btn-outline-primary rounded-pill" data-bs-dismiss="modal">
              Okay
            </button>
          </div>

        </div>
      </div>
    </div>

    <FloatingChatBot />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import CandidateNavbar from "../components/CandidateNavbar.vue";
import FloatingChatBot from "../components/ChatBot.vue";
import { marked } from "marked";
import Swal from "sweetalert2";

const API_BASE = "http://127.0.0.1:5000/api";

const savedJobs = ref([]);
const loading = ref(true);

const selectedJob = ref(null);
const jobForApply = ref(null);

let savedJobModalInstance = null;
let applyModalInstance = null;

const savedJobModalRef = ref(null);
const applyModalRef = ref(null);

// -------------------- UTILITIES --------------------
const formatExperience = (exp) => {
  if (!exp) return "Not specified";
  if (exp === 0) return "Fresher (0 yrs)";
  return exp + " years";
};

const formatReadableDate = (raw) => {
  if (!raw) return "Not specified";
  const d = new Date(raw);
  return d.toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

const getShortDescription = (t) => {
  if (!t) return "...";
  const plain = t.replace(/[#*_`>-]/g, " ").replace(/\s+/g, " ").trim();
  return plain.length > 120 ? plain.slice(0, 120) + "..." : plain;
};

const deriveJobSkills = (job) => {
  const text = (job.description || "").toLowerCase();
  const keywords = ["Python", "JavaScript", "VueJS", "SQL", "Flask", "React"];
  return keywords.filter((k) => text.includes(k.toLowerCase()));
};

const jobMarkdownHtml = computed(() => {
  if (!selectedJob.value) return "";
  return marked.parse(selectedJob.value.description || "");
});

// -------------------- LOAD SAVED JOB DATA --------------------
const loadSavedJobs = async () => {
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_BASE}/saved-jobs-details`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (data.success) {
      savedJobs.value = data.jobs;
    }
  } catch {
    Swal.fire("Error", "Unable to load saved jobs.", "error");
  }

  loading.value = false;
};

// -------------------- UNSAVE --------------------
const unsaveJob = async (job) => {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_BASE}/save-job/${job.job_id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await res.json();

  if (data.success) {
    // Remove from saved jobs page
    savedJobs.value = savedJobs.value.filter((j) => j.job_id !== job.job_id);

    // update global savedJobIds (sync with dashboard)
    const savedRaw = localStorage.getItem("candidate_saved_jobs");
    let updated = [];
    if (savedRaw) {
      updated = JSON.parse(savedRaw).filter((id) => id !== job.job_id);
    }
    localStorage.setItem("candidate_saved_jobs", JSON.stringify(updated));

    window.dispatchEvent(new CustomEvent("saved-jobs-updated"));

    Swal.fire({
      toast: true,
      icon: "info",
      title: "Removed from saved jobs",
      position: "top-end",
      showConfirmButton: false,
      timer: 1600,
    });
  }
};

// -------------------- OPEN MODALS --------------------
const openJobModal = (job) => {
  selectedJob.value = job;
  if (savedJobModalInstance) savedJobModalInstance.show();
};

const openApplyComingSoon = (job) => {
  jobForApply.value = job;
  if (applyModalInstance) applyModalInstance.show();
};

// -------------------- MOUNT --------------------
onMounted(() => {
  loadSavedJobs();

  savedJobModalInstance = new Modal(savedJobModalRef.value);
  applyModalInstance = new Modal(applyModalRef.value);
});
</script>

<style scoped>
.saved-jobs-page {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #e0edff, #eef4ff 40%, #e7f1ff 70%, #dde8ff);
}

/* Glass Card */
.glass-card {
  background: rgba(255, 255, 255, 0.92);
  border-radius: 1.25rem;
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

/* Job card */
.job-card {
  border-radius: 1.4rem;
  transition: 0.25s ease;
}
.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 35px rgba(15, 23, 42, 0.22);
}

/* Save/Unsave button */
.favorite-btn {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.55);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.favorite-btn-active {
  background: #e0f2fe;
  color: #0ea5e9;
  border-color: transparent;
}

/* Markdown styling */
.markdown-body {
  line-height: 1.5;
}
.markdown-body ul {
  padding-left: 1.2rem;
}

/* Modal */
.glass-modal {
  background: rgba(255, 255, 255, 0.96);
  border-radius: 1.4rem;
  backdrop-filter: blur(18px);
}

/* Fade */
.fade-in.visible {
  animation: fadeInUp 0.6s ease forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
