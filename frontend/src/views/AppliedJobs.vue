<template>
  <div class="applied-jobs-page">
    <CandidateNavbar />

    <section class="py-4 py-md-5">
      <div class="container">

        <!-- HEADER -->
        <div class="mb-4 fade-in">
          <h2 class="fw-bold text-primary mb-1">Your Applications</h2>
          <p class="text-muted small">Track your job application progress in real-time.</p>
        </div>

        <!-- SEARCH + FILTERS -->
        <div class="glass-card filter-card p-3 p-md-4 mb-4 fade-in">
          <div class="row g-3 align-items-center">

            <div class="col-lg-4">
              <label class="form-label small text-muted mb-1">Search</label>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control rounded-pill"
                placeholder="Role, company or location"
              />
            </div>

            <div class="col-lg-3">
              <label class="form-label small text-muted mb-1">Sort</label>
              <select v-model="sortOption" class="form-select rounded-pill">
                <option value="LATEST">Latest Applied</option>
                <option value="OLDEST">Oldest Applied</option>
                <option value="TITLE_ASC">Title A → Z</option>
                <option value="TITLE_DESC">Title Z → A</option>
              </select>
            </div>

            <div class="col-lg-3">
              <label class="form-label small text-muted mb-1">Status</label>
              <select v-model="statusFilter" class="form-select rounded-pill">
                <option value="">All</option>
                <option value="Applied">Applied</option>
                <option value="Shortlisted">Shortlisted</option>
                <option value="Test Completed">Test Completed</option>
                <option value="HR Review">HR Review</option>
                <option value="Selected">Selected</option>
                <option value="Rejected">Rejected</option>
              </select>
            </div>

          </div>
        </div>

        <!-- LOADING -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary"></div>
          <p class="text-muted small mt-2">Loading your applications...</p>
        </div>

        <!-- JOB LIST -->
        <div v-else>
          <div v-if="filteredJobs.length" class="row g-4 fade-in">

            <div v-for="job in filteredJobs" :key="job.job_id" class="col-md-6 col-lg-6">

              <!-- MODERN JOB CARD -->
              <div class="job-card-modern glass-card p-4 d-flex flex-column h-100">

                <!-- HEADER -->
                <div class="d-flex justify-content-between mb-3">

                  <!-- LEFT SECTION (Avatar + Info) -->
                  <div class="d-flex gap-3">

                    <!-- Avatar -->
                    <div class="job-avatar shadow-sm">
                      <img :src="generateJobAvatar(job.job_title)" />
                    </div>

                    <!-- Title / Company / Location -->
                    <div>
                      <h5 class="fw-bold text-dark mb-1 job-title">{{ job.job_title }}</h5>

                      <div class="text-primary fw-semibold small mb-1">
                        <i class="bi bi-building me-1"></i> {{ job.company }}
                      </div>

                      <div class="text-muted small">
                        <i class="bi bi-geo-alt me-1 text-primary"></i> {{ job.location }}
                      </div>
                    </div>
                  </div>
                  <div class="text-end ms-auto">
                    <span :class="['status-badge', normalizeStatus(job.status)]">
                      {{ job.status }}
                    </span>
                  </div>
              
                </div>


                <!-- APPLIED DATE -->
                <p class="small text-secondary border-start ps-2 mt-2 mb-0">
                  <i class="bi bi-calendar-check text-primary me-1"></i>
                  Applied on:
                  <span class="fw-semibold">{{ formatReadableDate(job.applied_on) }}</span>
                </p>

                <!-- PROGRESS PIPELINE -->
                <div class="progress-container mt-4">
                  <div
                    v-for="(stage, index) in stages"
                    :key="index"
                    class="progress-step"
                    :class="{
                      completed: index <= currentStageIndex(job),
                      final: isFinalStage(job, stage)
                    }"
                  >

                    <div class="step-icon-wrapper">
                      <div class="step-icon">
                        <i :class="stage.icon"></i>
                      </div>
                    </div>

                    <span class="step-label">{{ stage.label }}</span>

                    <!-- connector -->
                    <div v-if="index < stages.length - 1" class="step-line"></div>
                  </div>
                </div>

              </div>
            </div>

          </div>

          <!-- EMPTY STATE -->
          <div v-else class="text-center mt-5">
            <i class="bi bi-search fs-1 text-secondary"></i>
            <p class="text-muted mt-2">No job applications found.</p>
          </div>

        </div>

      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import CandidateNavbar from "../components/CandidateNavbar.vue";

const API_URL = "http://127.0.0.1:5000/api";

const loading = ref(false);
const appliedJobs = ref([]);

const searchQuery = ref("");
const sortOption = ref("LATEST");
const statusFilter = ref("");

/* -----------------------------------
   PIPELINE STAGES
----------------------------------- */
const stages = [
  { label: "Applied", icon: "bi bi-send" },
  { label: "Shortlisted", icon: "bi bi-stars" },
  { label: "Interview Scheduled", icon: "bi bi-calendar-event" },
  { label: "Interviewed", icon: "bi bi-pencil-square" },
  { label: "Offered", icon: "bi bi-briefcase" },
  { label: "Final", icon: "bi bi-flag" },
];

/* Avatar utils */
function getInitialsFromTitle(title) {
  if (!title) return "JD";
  const parts = title.trim().split(" ");
  return parts.length === 1
    ? (parts[0][0] + (parts[0][1] || "D")).toUpperCase()
    : (parts[0][0] + parts[1][0]).toUpperCase();
}

function generateJobAvatar(title) {
  const initials = getInitialsFromTitle(title);
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&background=3864f2&color=fff&rounded=true`;
}

/* Status utils */
function normalizeStatus(status) {
  return status.toLowerCase().replace(" ", "");
}

function currentStageIndex(job) {
  const status = (job.status || "").toUpperCase();

  switch (status) {
    case "APPLIED":
      return 0;

    case "SHORTLISTED":
      return 1;

    case "INTERVIEW_SCHEDULED":
      return 2;

    case "TEST_COMPLETED":
    case "HR_REVIEW":
    case "INTERVIEWED":
      return 3;

    case "OFFERED":
      return 4;

    case "SELECTED":
    case "REJECTED":
      return 5;

    default:
      return 0;
  }
}



function isFinalStage(job, stage) {
  const s = (job.status || "").toUpperCase();
  return stage.label === "Final" && (s === "SELECTED" || s === "REJECTED");
}


function formatReadableDate(date) {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

/* Fetch applications */
async function loadAppliedJobs() {
  loading.value = true;
  try {
    const res = await fetch(`${API_URL}/applied-jobs`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });
    const data = await res.json();
    appliedJobs.value = data.applications || [];
  } catch (err) {
    console.error("Failed to load applied jobs", err);
  }
  loading.value = false;
}

/* Filters */
const filteredJobs = computed(() => {
  let list = [...appliedJobs.value];

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(job =>
      job.job_title?.toLowerCase().includes(q) ||
      job.company?.toLowerCase().includes(q) ||
      job.location?.toLowerCase().includes(q)
    );
  }

  if (statusFilter.value) {
    list = list.filter(job => job.status === statusFilter.value);
  }

  if (sortOption.value === "LATEST") {
    list.sort((a, b) => new Date(b.applied_on) - new Date(a.applied_on));
  } else if (sortOption.value === "OLDEST") {
    list.sort((a, b) => new Date(a.applied_on) - new Date(b.applied_on));
  } else if (sortOption.value === "TITLE_ASC") {
    list.sort((a, b) => a.job_title.localeCompare(b.job_title));
  } else if (sortOption.value === "TITLE_DESC") {
    list.sort((a, b) => b.job_title.localeCompare(a.job_title));
  }

  return list;
});

onMounted(loadAppliedJobs);
</script>

<style scoped>
/* Background */
.applied-jobs-page {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #e8f0ff, #eef5ff);
}

/* Glass card */
.glass-card {
  border-radius: 1.4rem;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(210, 220, 240, 0.55);
  backdrop-filter: blur(14px);
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.08);
}

/* Job card */
.job-card-modern {
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(220, 227, 240, 0.65);
  backdrop-filter: blur(14px);
  transition: 0.25s ease;
}

.job-card-modern:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(25, 40, 70, 0.18);
}

/* Avatar */
.job-avatar {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  overflow: hidden;
  background: #eef4ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.job-title {
  font-size: 1.05rem;
  line-height: 1.3;
}

/* Pipeline */
.progress-container {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-top: 22px;
  padding: 0 4px; /* Slight extra spacing (Option B improvement) */
}

.progress-step {
  text-align: center;
  width: 20%;
  position: relative;
}

.step-icon-wrapper {
  display: flex;
  justify-content: center;
}

.step-icon {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  background: #e2e8f0;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  transition: 0.3s ease;
  z-index: 2;
  margin-bottom: 6px;
}

/* status badge */
.status-badge {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  white-space: nowrap;
}
.status-badge.applied { background: #dbeafe; color: #1e40af; }
.status-badge.shortlisted { background: #fef3c7; color: #92400e; }
.status-badge.testcompleted { background: #e0f2fe; color: #0369a1; }
.status-badge.hrreview { background: #e0f2fe; color: #0369a1; }
.status-badge.interviewed { background: #fde68a; color: #92400e; }
.status-badge.offered { background: #d1fae5; color: #166534; }
.status-badge.selected { background: #dcfce7; color: #166534; }
.status-badge.rejected { background: #fee2e2; color: #7f1d1d; }

/* Completed */
.progress-step.completed .step-icon {
  background: #4ade80;
  color: #fff;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.45);
}

/* Final */
.progress-step.final .step-icon {
  background: #facc15;
  color: #000;
}

/* Label */
.step-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #6b7280;
  margin-top: 4px;
}

/* Connector line */
.step-line {
  position: absolute;
  top: 24px;
  left: 50%;
  width: calc(100% + 6px); /* small spacing improvement */
  height: 3px;
  background: #d1d5db;
  z-index: 1;
}

.progress-step.completed + .step-line {
  background: #4ade80 !important;
}

/* Fade effect */
.fade-in {
  animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
