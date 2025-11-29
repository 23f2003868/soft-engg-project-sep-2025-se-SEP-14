<template>
  <section class="job-management-section py-5">
    <div class="container">

      <!-- Welcome + Stats -->
      <div class="mb-5 fade-in visible">
        <h2 class="fw-bold text-primary">Welcome, {{ recruiterName }}</h2>
        <p class="text-muted mb-4">Here is an overview of your hiring activity.</p>

        <div class="row g-3 mt-5">
          <div class="col-md-4 col-lg-2" v-for="card in statsCards" :key="card.title">
            <div class="p-3 rounded-4 shadow-sm bg-white text-center stats-box">
              <div class="stats-icon"></div>
              <div class="text-muted small mt-1">{{ card.title }}</div>
              <div class="fs-4 fw-bold mt-1">{{ card.value }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Header -->
      <div class="text-center mb-4 fade-in visible">
        <h2 class="fw-bold text-primary">Job Management</h2>
        <p class="text-muted">Manage all your posted jobs in one place</p>
      </div>

      <!-- Filters Row -->
      <div class="row align-items-center mb-4 g-2 fade-in visible filter-row">
        <div class="col-md-4">
          <input v-model="searchQuery" type="text" class="form-control"
            placeholder="Search by title or location..." />
        </div>

        <div class="col-md-3">
          <select v-model="statusFilter" class="form-select">
            <option value="ALL">All Jobs</option>
            <option value="ACTIVE">Active Only</option>
            <option value="INACTIVE">Inactive Only</option>
          </select>
        </div>

        <div class="col-md-3">
          <select v-model="sortOption" class="form-select">
            <option value="NEWEST">Newest First</option>
            <option value="OLDEST">Oldest First</option>
            <option value="CLOSING_SOON">Closing Soon</option>
            <option value="TITLE_ASC">Title A–Z</option>
          </select>
        </div>

        <!-- Add Job -->
        <div class="col-md-2 text-md-end text-start">
          <button class="btn btn-primary rounded-3 shadow-sm w-100" @click="openAddJobModal">
            <i class="bi bi-plus-circle me-2"></i> Add Job
          </button>
        </div>
      </div>

      <!-- Job List -->
      <div v-if="paginatedJobs.length" class="row g-4">
        <div v-for="job in paginatedJobs" :key="job.job_id"
          class="col-md-6 col-lg-4 fade-in visible">

          <div class="job-card glass-card rounded-4 p-4 h-100 d-flex flex-column">

            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="fw-bold text-dark mb-0">{{ job.job_title }}</h5>
              <span class="badge"
                :class="getJobStatus(job) === 'Active' ? 'bg-success' : 'bg-secondary'">
                {{ getJobStatus(job) }}
              </span>
            </div>

            <p class="text-muted mb-1">
              <i class="bi bi-geo-alt me-1 text-primary"></i> {{ job.location }}
            </p>

            <p class="text-muted mb-2">
              <i class="bi bi-briefcase me-1 text-primary"></i> {{ job.job_type }}
            </p>

            <p class="text-muted small mb-1">
              <strong>Start:</strong> {{ formatDate(job.start_date) }}
            </p>

            <p class="text-muted small mb-2">
              <strong>End:</strong> {{ formatDate(job.end_date) }}
            </p>

            <p class="small text-secondary flex-grow-1">
              {{ getShortDescription(job) }}
            </p>

            <button class="glass-btn-sm mt-2" @click="openFullDescription(job)">
              View Full Description
            </button>

            <div class="d-flex justify-content-between flex-wrap gap-2 mt-3">
              <button class="btn btn-outline-primary btn-sm" @click="openEditJob(job)">
                <i class="bi bi-pencil-square"></i> Edit
              </button>

              <button class="btn btn-outline-info btn-sm" @click="viewApplicants(job)">
                <i class="bi bi-people"></i> View Applicants
              </button>
            </div>

          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center text-muted fade-in visible mt-5">
        <i class="bi bi-briefcase fs-1 text-secondary d-block mb-2"></i>
        <p>No jobs posted yet. Add your first job.</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1"
        class="d-flex justify-content-center align-items-center gap-2 mt-4">

        <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage === 1"
          @click="currentPage--">Prev</button>

        <span class="small"> Page {{ currentPage }} of {{ totalPages }} </span>

        <button class="btn btn-sm btn-outline-secondary"
          :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div class="modal fade" id="jobModal" tabindex="-1" ref="jobModalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 border-0 shadow-lg glass-modal">

          <div class="modal-header">
            <h5 class="modal-title fw-bold">
              {{ editingJobId ? "Edit Job" : "Add New Job" }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="saveJob">

              <div class="mb-3">
                <label class="form-label">Job Title</label>
                <input v-model="form.job_title" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Location</label>
                <input v-model="form.location" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Job Type</label>
                <select v-model="form.job_type" class="form-select" required>
                  <option value="">Select Type</option>
                  <option>Full-time</option>
                  <option>Part-time</option>
                  <option>Internship</option>
                </select>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Start Date</label>
                  <input v-model="form.start_date" type="date" class="form-control" required />
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label">End Date</label>
                  <input v-model="form.end_date" type="date" class="form-control" required />
                </div>
              </div>

              <div v-if="editingJobId" class="mb-3">
                <label class="form-label">Job Description</label>
                <textarea v-model="form.description" rows="4" class="form-control"
                  placeholder="Edit job description..." required></textarea>
              </div>

              <div v-if="!editingJobId" class="mb-3">
                <label class="form-label">Keywords (AI Description Generator)</label>
                <textarea v-model="form.description_keywords" rows="2" class="form-control"
                  placeholder="e.g., React, UI, MongoDB" required></textarea>
              </div>

              <div class="text-end">
                <button class="btn btn-primary rounded-3" type="submit">
                  {{ editingJobId ? "Update Job" : "Add Job" }}
                </button>
              </div>

            </form>
          </div>

        </div>
      </div>
    </div>

    <!-- Full Description Modal -->
    <div class="modal fade" id="fullDescModal" tabindex="-1" ref="fullDescModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4 shadow glass-modal">

          <div class="modal-header">
            <h5 class="modal-title fw-bold">{{ fullDescriptionJob?.job_title }} — Full Description</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="formatted-description"
              v-html="marked(fullDescriptionJob?.description || '')">
            </div>
          </div>

        </div>
      </div>
    </div>

  </section>
</template>



<script setup>
/* 🔥 YOUR SCRIPT — NOT MODIFIED AT ALL */
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";

const jobs = ref([]);
const recruiterName = localStorage.getItem("firstname") || "Recruiter";

const form = ref({
  job_title: "",
  location: "",
  job_type: "",
  description_keywords: "",
  start_date: "",
  end_date: "",
  description: "",
});

const editingJobId = ref(null);
const jobModalRef = ref(null);
const fullDescModalRef = ref(null);

let jobModalInstance = null;
let fullDescModalInstance = null;

const searchQuery = ref("");
const statusFilter = ref("ALL");
const sortOption = ref("NEWEST");

const currentPage = ref(1);
const pageSize = 6;

const API_BASE = "http://127.0.0.1:5000/api";

const statsCards = ref([
  { title: "Total Jobs", value: 0 },
  { title: "Active Jobs", value: 0 },
  { title: "Expired Jobs", value: 0 },
  { title: "Total Applicants", value: 0 },
  { title: "Shortlisted", value: 0 },
  { title: "Interviews", value: 0 },
]);

const formatDate = (d) => (d ? d.toString().slice(0, 10) : "-");

const getJobStatus = (job) => {
  const status = (job.status || "").toUpperCase();
  if (status === "INACTIVE" || status === "INACTV") return "Inactive";

  const today = new Date().toISOString().slice(0, 10);
  if (job.end_date < today) return "Inactive";

  return "Active";
};

const getShortDescription = (job) => {
  if (!job.description) return "";
  const html = marked(job.description);
  const plain = html.replace(/<[^>]+>/g, "");
  return plain.slice(0, 150) + "...";
};

const updateJobStats = () => {
  const total = jobs.value.length;
  const active = jobs.value.filter((j) => getJobStatus(j) === "Active").length;
  statsCards.value[0].value = total;
  statsCards.value[1].value = active;
  statsCards.value[2].value = total - active;
};

const loadJobs = async () => {
  try {
    const res = await fetch(`${API_BASE}/jobs`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });

    const data = await res.json();
    if (res.ok) {
      jobs.value = data.jobs || [];
      updateJobStats();
      currentPage.value = 1;
    }
  } catch {}
};

const fullDescriptionJob = ref(null);
const openFullDescription = (job) => {
  fullDescriptionJob.value = job;
  fullDescModalInstance.show();
};

const filteredJobs = computed(() => {
  const q = searchQuery.value.toLowerCase();

  return jobs.value.filter((job) => {
    const match =
      job.job_title.toLowerCase().includes(q) ||
      job.location.toLowerCase().includes(q);

    const status = getJobStatus(job);
    if (statusFilter.value === "ACTIVE" && status !== "Active") return false;
    if (statusFilter.value === "INACTIVE" && status !== "Inactive") return false;

    return match;
  });
});

const sortedJobs = computed(() => {
  const list = [...filteredJobs.value];

  if (sortOption.value === "NEWEST") return list.sort((a, b) => b.start_date.localeCompare(a.start_date));
  if (sortOption.value === "OLDEST") return list.sort((a, b) => a.start_date.localeCompare(b.start_date));
  if (sortOption.value === "CLOSING_SOON") return list.sort((a, b) => a.end_date.localeCompare(b.end_date));
  if (sortOption.value === "TITLE_ASC") return list.sort((a, b) => a.job_title.localeCompare(b.job_title));

  return list;
});

const totalPages = computed(() =>
  Math.ceil(sortedJobs.value.length / pageSize)
);

const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return sortedJobs.value.slice(start, start + pageSize);
});

const openAddJobModal = () => {
  form.value = {
    job_title: "",
    location: "",
    job_type: "",
    description_keywords: "",
    start_date: "",
    end_date: "",
    description: "",
  };
  editingJobId.value = null;
  jobModalInstance.show();
};

const openEditJob = (job) => {
  form.value = {
    job_title: job.job_title,
    location: job.location,
    job_type: job.job_type,
    description_keywords: "",
    start_date: formatDate(job.start_date),
    end_date: formatDate(job.end_date),
    description: job.description || "",
  };
  editingJobId.value = job.job_id;
  jobModalInstance.show();
};

const saveJob = async () => {
  if (form.value.end_date < form.value.start_date)
    return Swal.fire("Error", "End date cannot be earlier than start date.", "error");

  const payload = editingJobId.value
    ? {
        job_title: form.value.job_title,
        location: form.value.location,
        job_type: form.value.job_type,
        start_date: form.value.start_date,
        end_date: form.value.end_date,
        description: form.value.description,
      }
    : {
        job_title: form.value.job_title,
        location: form.value.location,
        job_type: form.value.job_type,
        start_date: form.value.start_date,
        end_date: form.value.end_date,
        description_keywords: form.value.description_keywords,
      };

  const url = editingJobId.value
    ? `${API_BASE}/job/${editingJobId.value}`
    : `${API_BASE}/job`;

  const method = editingJobId.value ? "PUT" : "POST";

  try {
    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      Swal.fire("Error", data.message || "Save failed", "error");
      return;
    }

    Swal.fire("Success", editingJobId.value ? "Job updated" : "Job created", "success");
    jobModalInstance.hide();
    await loadJobs();

  } catch {
    Swal.fire("Error", "Server error", "error");
  }
};

const viewApplicants = () => {
  Swal.fire("Coming Soon", "Applicant list feature is coming soon!", "info");
};

onMounted(() => {
  jobModalInstance = new Modal(jobModalRef.value);
  fullDescModalInstance = new Modal(fullDescModalRef.value);
  loadJobs();
});
</script>



<style scoped>

/* ------------------------------ */
/* Background + Layout            */
/* ------------------------------ */
.job-management-section {
  min-height: calc(100vh - 80px);
  background: linear-gradient(120deg, #eef4ff, #e6f0ff);
}

/* ------------------------------ */
/* Fade-in Animation              */
/* ------------------------------ */
.fade-in.visible {
  animation: fadeInUp 0.7s ease forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ====================================================== */
/*  MODERN STATS CARDS                                    */
/* ====================================================== */

.stats-box {
  position: relative;
  padding-top: 58px !important;
  border-radius: 1.25rem;

  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);

  border: 3px solid transparent;
  background-clip: padding-box, border-box;
  background-origin: padding-box, border-box;
  background-image:
    linear-gradient(white, white),
    linear-gradient(135deg, #0072ff, #00c6ff, #5ce1e6);

  animation: borderGlow 6s linear infinite;

  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.12);

  transition: 0.35s ease;
}

/* Hover */
.stats-box:hover {
  transform: translateY(-8px);
  box-shadow: 0 18px 44px rgba(15, 23, 42, 0.28);
}

/* Animated Border */
@keyframes borderGlow {
  0% { background-image:
       linear-gradient(white, white),
       linear-gradient(135deg, #0072ff, #00c6ff, #5ce1e6); }
  50% { background-image:
       linear-gradient(white, white),
       linear-gradient(135deg, #00c6ff, #0072ff, #5ce1e6); }
  100% { background-image:
       linear-gradient(white, white),
       linear-gradient(135deg, #0072ff, #00c6ff, #5ce1e6); }
}

/* ---------------------------------- */
/* ICON BOX (Bootstrap Icons)         */
/* ---------------------------------- */

.stats-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;

  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);

  background: linear-gradient(135deg, #0072ff, #00c6ff);
  box-shadow: 0 6px 14px rgba(0, 114, 255, 0.32);

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 24px;
  color: white;

  transition: 0.35s ease;
}

/* ICON HOVER ANIMATION */
.stats-box:hover .stats-icon {
  transform: translateX(-50%) translateY(-4px) scale(1.18) rotate(4deg);
  box-shadow: 0 10px 26px rgba(0, 114, 255, 0.45);
}

/* ICON BASE */
.stats-icon::before {
  content: "";
  width: 24px;
  height: 24px;
  display: block;
  background: white;
  mask-size: contain;
  -webkit-mask-size: contain;
  mask-repeat: no-repeat;
  -webkit-mask-repeat: no-repeat;
  mask-position: center;
  -webkit-mask-position: center;
}

/* 1️⃣ Total Jobs */
.col-md-4.col-lg-2:nth-child(1) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/collection.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/collection.svg");
}

/* 2️⃣ Active Jobs */
.col-md-4.col-lg-2:nth-child(2) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/lightning-charge-fill.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/lightning-charge-fill.svg");
}

/* 3️⃣ Expired Jobs */
.col-md-4.col-lg-2:nth-child(3) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/hourglass-split.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/hourglass-split.svg");
}

/* 4️⃣ Total Applicants */
.col-md-4.col-lg-2:nth-child(4) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/people-fill.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/people-fill.svg");
}

/* 5️⃣ Shortlisted */
.col-md-4.col-lg-2:nth-child(5) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/star-fill.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/star-fill.svg");
}

/* 6️⃣ Interviews */
.col-md-4.col-lg-2:nth-child(6) .stats-icon::before {
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/mic-fill.svg");
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/mic-fill.svg");
}

/* ------------------------------ */
/* Filters                        */
/* ------------------------------ */
.filter-row .form-control,
.filter-row .form-select {
  height: 46px;
  border-radius: 12px;
  border: 1.5px solid #d4d9e1;
  background: rgba(255, 255, 255, 0.9);
  transition: 0.2s ease;
}

.filter-row .form-control:focus,
.filter-row .form-select:focus {
  border-color: #0072ff;
  box-shadow: 0 0 0 0.15rem rgba(0, 114, 255, 0.2);
}

/* ------------------------------ */
/* Glass Cards                    */
/* ------------------------------ */
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);
  border-radius: 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.16);
  transition: 0.3s ease;
}

.job-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.22);
}

/* Glass Modal */
.glass-modal {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(22px);
  border-radius: 1.25rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Glass Button */
.glass-btn-sm {
  padding: 8px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(13, 110, 253, 0.3);
  font-size: 0.82rem;
  font-weight: 600;
  color: #0072ff;
  transition: 0.2s ease;
}

.glass-btn-sm:hover {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(13, 110, 253, 0.35);
}

/* Pagination */
.btn-sm {
  border-radius: 999px;
}

</style>
