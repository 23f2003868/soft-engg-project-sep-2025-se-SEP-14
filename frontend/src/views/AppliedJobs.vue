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

        <!-- SEARCH & FILTERS -->
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

        <!-- LOADING STATE -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary"></div>
          <p class="text-muted small mt-2">Loading your applications...</p>
        </div>

        <!-- JOB LIST -->
        <div v-else>
          <div v-if="filteredJobs.length" class="row g-4 fade-in">

            <div
              v-for="job in filteredJobs"
              :key="job.job_id"
              class="col-md-6 col-lg-4"
            >
              <!-- MODERN JOB CARD -->
              <div class="job-card-modern p-4">

                <!-- Title + Status -->
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h5 class="fw-bold job-title">{{ job.job_title }}</h5>
                    <div class="text-muted small d-flex align-items-center">
                      <i class="bi bi-geo-alt me-1 text-primary"></i>
                      {{ job.location }}
                    </div>
                  </div>

                  <!-- STATUS BADGE -->
                  <span :class="['status-badge', normalizeStatus(job.status)]">
                    {{ job.status }}
                  </span>
                </div>

                <!-- APPLIED DATE -->
                <p class="small text-secondary mt-2">
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

                    <div class="step-icon">
                      <i :class="stage.icon"></i>
                    </div>

                    <span class="step-label">{{ stage.label }}</span>

                    <div v-if="index < stages.length - 1" class="step-line"></div>
                  </div>

                </div>

              </div>
            </div>

          </div>

          <!-- EMPTY -->
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
   HIRING PIPELINE STAGES
----------------------------------- */
const stages = [
  { label: "Applied", icon: "bi bi-send" },
  { label: "Shortlisted", icon: "bi bi-stars" },
  { label: "Interviwed", icon: "bi bi-pencil-square" },
  { label: "Offered", icon: "bi bi-person-lines-fill" },
  { label: "Final", icon: "bi bi-flag" },
];

/* Normalize backend statuses */
function normalizeStatus(status) {
  return status.toLowerCase().replace(" ", "");
}

/* Determine stage index */
function currentStageIndex(job) {
  switch (job.status) {
    case "Applied": return 0;
    case "Shortlisted": return 1;
    case "Tested":
    case "Test Completed": return 2;
    case "HR Review": return 3;
    case "Selected":
    case "Rejected": return 4;
    default: return 0;
  }
}

function isFinalStage(job, stage) {
  return stage.label === "Final" && ["Selected", "Rejected"].includes(job.status);
}

/* Format date */
function formatReadableDate(date) {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

/* Fetch applied jobs */
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

/* Filters + Sorting */
const filteredJobs = computed(() => {
  let list = [...appliedJobs.value];

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(job =>
      job.job_title?.toLowerCase().includes(q) ||
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
/* PAGE BACKGROUND */
.applied-jobs-page {
  background: radial-gradient(circle at top left, #e8f0ff, #eef5ff);
  min-height: 100vh;
}

/* GLASS FILTER CARD */
.glass-card {
  border-radius: 1.4rem;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
}

/* MODERN JOB CARD */
.job-card-modern {
  background: white;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  transition: 0.25s ease;
}

.job-card-modern:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
}

/* STATUS BADGES */
.status-badge {
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.4px;
}

.status-badge.applied {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.shortlisted {
  background: #fef9c3;
  color: #b45309;
}

.status-badge.testcompleted,
.status-badge.tested {
  background: #e0f2fe;
  color: #0369a1;
}

.status-badge.hrreview {
  background: #ede9fe;
  color: #5b21b6;
}

.status-badge.selected {
  background: #dcfce7;
  color: #15803d;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #b91c1c;
}

/* PROGRESS PIPELINE */
.progress-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
}

.step-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #e5e7eb;
  color: #374151;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: 0.3s ease;
  z-index: 2;
}

.progress-step.completed .step-icon {
  background: #4ade80;
  color: white;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.progress-step.final .step-icon {
  background: #facc15;
  color: #000;
}

.step-label {
  margin-top: 6px;
  font-size: 0.72rem;
  color: #6b7280;
  text-align: center;
}

/* Connecting lines */
.step-line {
  position: absolute;
  top: 18px;
  left: 50%;
  width: 100%;
  height: 3px;
  background: #e5e7eb;
  z-index: 1;
}

.progress-step.completed ~ .step-line {
  background: #4ade80;
}

/* Animation */
.fade-in {
  animation: fadeInUp 0.55s ease;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
