<template>
  <section class="rec-dashboard py-5">
    <div class="container">

      <!-- HEADER (now full width on its own row) -->
      <div class="row mb-3">
        <div class="col-12">
          <h2 class="fw-bold mb-1">👋 Welcome, {{ recruiterName }}</h2>
          <p class="text-muted mb-0">Overview of your hiring activity — updated live.</p>
        </div>
      </div>

      <!-- STATS ROW (moved to its own row below header) -->
      <div class="row mb-5 mt-5">
        <div class="col-12">
          <div class="d-flex justify-content-between flex-wrap stats-row">
            <div
              v-for="card in statsCards"
              :key="card.key"
              class="stats-card d-flex flex-column align-items-start justify-content-center"
              :title="card.title"
              tabindex="0"
            >
              <div class="d-flex w-100 justify-content-between align-items-start">
                <div class="text-start">
                  <div class="small text-muted mb-1">{{ card.title }}</div>
                  <div class="fw-bold fs-5">{{ card.value }}</div>
                </div>
                <div class="stats-icon-wrapper ms-3">
                  <i :class="'bi ' + card.icon"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTROLS: Search / Filters / Add Job -->
      <div class="row align-items-center mb-4 g-2">
        <div class="col-md-5">
          <div class="input-group search-input">
            <span class="input-group-text bg-white border-0">
              <i class="bi bi-search text-primary"></i>
            </span>
            <input
              v-model="searchQuery"
              @input="debouncedFilter"
              type="search"
              class="form-control form-control-lg border-0"
              placeholder="Search job title, location or keywords..."
              aria-label="Search jobs"
            />
            <button v-if="searchQuery" class="btn btn-sm btn-outline-secondary me-1" @click="clearSearch">Clear</button>
          </div>
        </div>

        <div class="col-md-3">
          <select v-model="statusFilter" class="form-select form-select-lg rounded-pill">
            <option value="ALL">All Jobs</option>
            <option value="ACTIVE">Active</option>
            <option value="INACTIVE">Expired</option>
          </select>
        </div>

        <div class="col-md-2">
          <select v-model="jobTypeFilter" class="form-select form-select-lg rounded-pill">
            <option value="">All Types</option>
            <option value="Full-time">Full-time</option>
            <option value="Part-time">Part-time</option>
            <option value="Internship">Internship</option>
            <option value="Contract">Contract</option>
            <option value="Remote">Remote</option>
          </select>
        </div>

        <div class="col-md-2 text-md-end">
          <!-- single Add Job button -->
          <button class="btn btn-primary btn-lg rounded-pill" @click="openAddJobModal">
            <i class="bi bi-plus-circle me-2"></i> Add Job
          </button>
        </div>
      </div>

      <!-- JOB CARDS -->
      <div class="row g-4">
        <div v-if="jobs.length === 0" class="text-center py-5 w-100">
          <i class="bi bi-folder-x fs-1 text-muted mb-2"></i>
          <p class="text-muted mb-0">No jobs posted yet</p>
        </div>

        <div v-else class="col-lg-4 col-md-6" v-for="job in paginatedJobs" :key="job.job_id">
          <article class="job-card card shadow-sm p-3 h-100 d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start">
              <div class="d-flex align-items-start gap-3">
                <div class="job-avatar">
                  <img :src="generateJobAvatar(job.job_title)" :alt="job.job_title" />
                </div>
                <div>
                  <h5 class="job-title mb-1">{{ job.job_title }}</h5>
                  <div class="text-muted small">
                    <strong class="company-name">{{ recruiterName }}</strong>
                    <span class="ms-2">•</span>
                    <span class="ms-2"><i class="bi bi-geo-alt me-1 text-primary"></i>{{ job.location || "Remote/Not specified" }}</span>
                  </div>
                </div>
              </div>

              <div class="text-end">
                <span :class="['badge', getJobStatus(job) === 'Active' ? 'bg-success' : 'bg-secondary']">
                  {{ getJobStatus(job) }}
                </span>
                <div class="text-muted small mt-1">{{ job.job_type || "Not specified" }}</div>
              </div>
            </div>

            <div class="mt-2 small text-muted">
              <i class="bi bi-clock-history me-1"></i>
              <span>Experience: <strong>{{ formatExperience(job.experience) }}</strong></span>
              <span class="mx-2">•</span>
              <span>End: {{ formatDate(job.end_date) }}</span>
            </div>

            <div class="my-3 job-desc text-secondary">
              <!-- markdown excerpt -->
              <div v-html="renderExcerpt(job.description)"></div>
            </div>

            <div class="d-flex flex-wrap gap-2 mb-3">
              <span v-for="s in deriveJobSkills(job)" :key="s" class="badge bg-light text-primary border small-pill">{{ s }}</span>
            </div>

            <div class="d-flex justify-content-between align-items-center mt-auto">
              <div class="d-flex gap-2 align-items-center">
                <button class="btn btn-outline-primary btn-sm rounded-pill action-btn" @click="openFullDescription(job)">Full Description</button>
                <button class="btn btn-outline-secondary btn-sm rounded-pill action-btn" @click="viewApplicants(job)"><i class="bi bi-people me-1"></i>Applicants</button>
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-light btn-sm border rounded-pill action-btn" @click="openEditJob(job)"><i class="bi bi-pencil-square"></i> Edit</button>
                <button class="btn btn-danger btn-sm rounded-pill action-btn" @click="confirmDelete(job)"><i class="bi bi-trash"></i> Delete</button>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- PAGINATION -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
        <button class="btn btn-sm btn-outline-secondary me-2" :disabled="currentPage === 1" @click="currentPage--">Prev</button>
        <span class="align-self-center">Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="btn btn-sm btn-outline-secondary ms-2" :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
      </div>
    </div>

    <!-- FULL DESCRIPTION MODAL -->
    <div class="modal fade" ref="fullDescModalRef" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content rounded-4 shadow-lg">
          <div class="modal-header">
            <div>
              <h5 class="modal-title">{{ fullDescriptionJob?.job_title }}</h5>
              <div class="small text-muted">{{ recruiterName }} • {{ fullDescriptionJob?.location }}</div>
            </div>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-html="renderFullDescription(fullDescriptionJob?.description)"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ADD JOB MODAL -->
    <div class="modal fade" ref="addJobModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4 shadow-lg p-2">
          <div class="modal-header border-0">
            <h5 class="modal-title fw-bold">Add New Job</h5>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Job Title</label>
                <input v-model="newJob.job_title" class="form-control" placeholder="e.g. Senior Backend Engineer" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Location</label>
                <input v-model="newJob.location" class="form-control" placeholder="City, Remote or Hybrid" />
              </div>

              <div class="col-md-4">
                <label class="form-label">Job Type</label>
                <select v-model="newJob.job_type" class="form-select">
                  <option value="">Select type</option>
                  <option value="Full-time">Full-time</option>
                  <option value="Part-time">Part-time</option>
                  <option value="Internship">Internship</option>
                  <option value="Contract">Contract</option>
                  <option value="Remote">Remote</option>
                </select>
              </div>

              <div class="col-md-4">
                <label class="form-label">Experience (years)</label>
                <input v-model.number="newJob.experience" type="number" min="0" class="form-control" placeholder="0" />
              </div>

              <div class="col-md-4">
                <label class="form-label">Start Date</label>
                <input v-model="newJob.start_date" type="date" :min="today" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">End Date</label>
                <input v-model="newJob.end_date" type="date" :min="newJob.start_date || today" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Description keywords</label>
                <input v-model="newJob.description_keywords" class="form-control" placeholder="Comma separated: python, ai, flask" />
                <small class="text-muted">AI will generate the full markdown description from these keywords.</small>
              </div>
            </div>
          </div>

          <div class="modal-footer border-0">
            <button class="btn btn-secondary rounded-pill" :disabled="creatingJob" data-bs-dismiss="modal">Cancel</button>
            <button class="btn btn-primary rounded-pill" :disabled="creatingJob" @click="createJob">
              <span v-if="creatingJob" class="spinner-border spinner-border-sm me-2"></span>
              {{ creatingJob ? "Creating..." : "Create Job" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- EDIT JOB MODAL (with live markdown preview and start-date editable) -->
    <div class="modal fade" ref="editJobModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4 shadow-lg">
          <div class="modal-header">
            <h5 class="modal-title">Edit Job</h5>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Job Title</label>
                <input v-model="editJob.job_title" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Location</label>
                <input v-model="editJob.location" class="form-control" />
              </div>

              <div class="col-md-4">
                <label class="form-label">Job Type</label>
                <select v-model="editJob.job_type" class="form-select">
                  <option value="">Select type</option>
                  <option value="Full-time">Full-time</option>
                  <option value="Part-time">Part-time</option>
                  <option value="Internship">Internship</option>
                  <option value="Contract">Contract</option>
                  <option value="Remote">Remote</option>
                </select>
              </div>

              <div class="col-md-4">
                <label class="form-label">Experience (years)</label>
                <input v-model.number="editJob.experience" type="number" min="0" class="form-control" />
              </div>

              <div class="col-md-4">
                <label class="form-label">Start Date</label>
                <input v-model="editJob.start_date" type="date" :max="editJob.end_date || ''" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">End Date</label>
                <input v-model="editJob.end_date" type="date" :min="editJob.start_date || today" class="form-control" />
              </div>

              <div class="col-12">
                <label class="form-label">Description (markdown)</label>
                <textarea v-model="editJob.description" rows="6" class="form-control" placeholder="Markdown content appears here..."></textarea>
                <small class="text-muted">You can edit markdown here; preview updates below.</small>
              </div>

              <div class="col-12 mt-3">
                <label class="form-label">Live Preview</label>
                <div class="preview-box p-3 border rounded" v-html="editJobPreviewHtml"></div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Cancel</button>
            <button class="btn btn-primary rounded-pill" @click="updateJob" :disabled="updatingJob">
              <span v-if="updatingJob" class="spinner-border spinner-border-sm me-2"></span>
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Applicants modal component (unchanged) -->
    <ApplicantsModal ref="applicantsModalComponent" />
  </section>
</template>

<script setup>
/* RecruiterDashboard.vue - polished & responsive
   Uses existing backend endpoints (unchanged).
   Key changes: improved UI, single Add button, live markdown preview, experience fix, debounce (no lodash).
*/

import { ref, computed, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";

import ApplicantsModal from "../components/ApplicantsModal.vue";

const API_BASE = "http://127.0.0.1:5000/api";
const recruiterName = localStorage.getItem("firstname") || (localStorage.getItem("company") || "Recruiter");

const today = new Date().toISOString().slice(0, 10);

// state
const jobs = ref([]);
const fullDescriptionJob = ref(null);

const searchQuery = ref("");
const statusFilter = ref("ALL");
const jobTypeFilter = ref("");
const sortOption = ref("NEWEST");
const currentPage = ref(1);
const pageSize = 9;

const creatingJob = ref(false);
const creatingError = ref("");
const newJob = ref({
  job_title: "",
  location: "",
  job_type: "",
  experience: 0,
  description_keywords: "",
  start_date: today,
  end_date: ""
});

// editing
const editJob = ref({});
const updatingJob = ref(false);

// modals
let addJobModal = null;
const addJobModalRef = ref(null);
let editJobModal = null;
const editJobModalRef = ref(null);
let fullDescModalInstance = null;
const fullDescModalRef = ref(null);

// stats
const statsCards = ref([
  { key: "jobs_posted", title: "Jobs Posted", value: 0, icon: "bi-briefcase" },
  { key: "active_jobs", title: "Active Jobs", value: 0, icon: "bi-lightning" },
  { key: "expired_jobs", title: "Expired Jobs", value: 0, icon: "bi-hourglass-split" },
  { key: "total_applicants", title: "Total Applicants", value: 0, icon: "bi-people" },
  { key: "shortlisted", title: "Shortlisted", value: 0, icon: "bi-person-check" },
  { key: "hired", title: "Hired", value: 0, icon: "bi-award" }
]);

// pagination / computed
const filteredJobs = computed(() => {
  let list = jobs.value.slice();

  // text search
  const q = (searchQuery.value || "").trim().toLowerCase();
  if (q) {
    list = list.filter(j =>
      (j.job_title || "").toLowerCase().includes(q) ||
      (j.location || "").toLowerCase().includes(q) ||
      (String(j.description || "")).toLowerCase().includes(q)
    );
  }

  // status filter
  const todayIso = new Date().toISOString().slice(0,10);
  if (statusFilter.value === "ACTIVE") list = list.filter(j => (j.end_date || "") >= todayIso);
  if (statusFilter.value === "INACTIVE") list = list.filter(j => (j.end_date || "") < todayIso);

  // job type filter
  if (jobTypeFilter.value) list = list.filter(j => (j.job_type || "") === jobTypeFilter.value);

  // sort
  if (sortOption.value === "NEWEST") list.sort((a,b) => (b.start_date || "").localeCompare(a.start_date || ""));
  else if (sortOption.value === "OLDEST") list.sort((a,b) => (a.start_date || "").localeCompare(b.start_date || ""));
  else if (sortOption.value === "TITLE_ASC") list.sort((a,b) => (a.job_title || "").localeCompare(b.job_title || ""));

  return list;
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredJobs.value.length / pageSize)));
const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredJobs.value.slice(start, start + pageSize);
});

// small utility dependencies (no lodash)
function debounce(fn, wait = 250) {
  let t = null;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

const debouncedFilter = debounce(() => {
  currentPage.value = 1;
});

// open modals
onMounted(() => {
  nextTick(() => {
    if (addJobModalRef.value) {
      addJobModal = new Modal(addJobModalRef.value, {
        backdrop: "static",
        keyboard: false
      });
    }

    if (editJobModalRef.value) {
      editJobModal = new Modal(editJobModalRef.value, {
        backdrop: "static",
        keyboard: false
      });
    }

    if (fullDescModalRef.value) {
      fullDescModalInstance = new Modal(fullDescModalRef.value, {
        backdrop: "static",
        keyboard: false
      });
    }
  });

  loadJobs();
  loadRecruiterStats();
});


async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/recruiter/jobs`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const data = await res.json();
    if (res.ok) {
      jobs.value = data.jobs || [];
    } else {
      jobs.value = [];
      console.error("Failed to load recruiter jobs", data);
      Swal.fire("Error", data.message || "Failed to load jobs", "error");
    }
    refreshStatsFromJobs();
  } catch (e) {
    console.error(e);
    Swal.fire("Error", "Server error while fetching jobs", "error");
  }
}

async function loadRecruiterStats() {
  try {
    const res = await fetch(`${API_BASE}/recruiter/stats`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }});
    const data = await res.json();
    if (res.ok) {
      const map = {
        total_jobs: data.total_jobs ?? 0,
        total_applicants: data.total_applicants ?? 0,
        total_shortlisted: data.total_shortlisted ?? 0,
        total_hired: data.total_hired ?? 0
      };
      statsCards.value.find(c => c.key === "jobs_posted").value = map.total_jobs;
      statsCards.value.find(c => c.key === "total_applicants").value = map.total_applicants;
      statsCards.value.find(c => c.key === "shortlisted").value = map.total_shortlisted;
      statsCards.value.find(c => c.key === "hired").value = map.total_hired;
    }
  } catch (err) {
    console.error("loadRecruiterStats", err);
  }
}

function refreshStatsFromJobs() {
  const todayIso = new Date().toISOString().slice(0,10);
  const total = jobs.value.length;
  const active = jobs.value.filter(j => (j.end_date || "") >= todayIso).length;
  const expired = jobs.value.filter(j => (j.end_date || "") < todayIso).length;

  const jobsCard = statsCards.value.find(c => c.key === "jobs_posted");
  const activeCard = statsCards.value.find(c => c.key === "active_jobs");
  const expiredCard = statsCards.value.find(c => c.key === "expired_jobs");
  if (jobsCard) jobsCard.value = total;
  if (activeCard) activeCard.value = active;
  if (expiredCard) expiredCard.value = expired;
}

// helpers
const formatDate = (d) => (d ? String(d).slice(0,10) : "-");
const formatExperience = (exp) => {
  if (exp === null || exp === undefined || exp === "") return "Not specified";
  const n = Number(exp);
  if (Number.isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher (0 yrs)";
  if (n === 1) return "1 year";
  return `${n} years`;
};
const getJobStatus = (j) => ((j && j.end_date && j.end_date < new Date().toISOString().slice(0,10)) ? "Expired" : "Active");

// Skill derive simple function (keeps previous approach)
const allSkills = ["Python","SQL","VueJS","JavaScript","React","Node.js","Django","Flask","Machine Learning","Data Analysis"];
const deriveJobSkills = (job) => {
  if (!job) return [];
  const text = (job.description || "").toLowerCase();
  const skillsSet = new Set();
  allSkills.forEach(s => { if (text.includes(s.toLowerCase())) skillsSet.add(s); });
  if (skillsSet.size === 0) return ["Communication","Teamwork"];
  return Array.from(skillsSet).slice(0,6);
};

// excerpts + full markdown rendering
const renderExcerpt = (md) => {
  if (!md) return "<p class='text-muted small'>No description available.</p>";
  const plain = String(md).replace(/[#*_`>-]/g," ").replace(/\[(.*?)\]\((.*?)\)/g,"$1").replace(/\s+/g," ").trim();
  const short = (plain.length > 180) ? (plain.slice(0,180) + "...") : plain;
  return `<p class="mb-0 small text-secondary">${escapeHtml(short)}</p>`;
};
const renderFullDescription = (md) => {
  if (!md) return "<p>No description provided.</p>";
  try { return marked.parse(String(md)); } catch (e) { return `<pre>${escapeHtml(String(md))}</pre>`; }
};
function escapeHtml(s) { if (!s) return ""; return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;"); }

// open/edit/delete handlers
const openAddJobModal = () => {
  newJob.value = { job_title: "", location: "", job_type: "", experience: 0, description_keywords: "", start_date: today, end_date: "" };
  creatingJob.value = false;
  if (addJobModal) addJobModal.show();
};

const openEditJob = (job) => {
  // ensure experience numeric and include start_date
  editJob.value = { ...job, experience: Number(job.experience || 0), start_date: job.start_date || today };
  updatingJob.value = false;
  nextTick(() => {
    if (editJobModalRef.value) {
      if (!editJobModal) editJobModal = new Modal(editJobModalRef.value);
      editJobModal.show();
    }
  });
};

const confirmDelete = (job) => {
  Swal.fire({
    title: "Delete job?",
    text: job.job_title,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Delete"
  }).then(res => {
    if (res.isConfirmed) deleteJob(job.job_id);
  });
};

async function deleteJob(id) {
  try {
    const res = await fetch(`${API_BASE}/job/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const data = await res.json().catch(()=>({}));
    if (!res.ok) {
      Swal.fire("Error", data.message || "Failed to delete job", "error");
      return;
    }
    Swal.fire("Deleted", "Job removed", "success");
    await loadJobs();
    await loadRecruiterStats();
  } catch (err) {
    Swal.fire("Error", "Server error", "error");
  }
}

// create job - uses backend Gemini flow (server will generate description)
async function createJob() {
  creatingJob.value = true;
  try {
    // basic validation
    if (!newJob.value.job_title || !newJob.value.location || !newJob.value.start_date || !newJob.value.end_date) {
      Swal.fire("Validation", "Please fill required fields", "warning");
      creatingJob.value = false;
      return;
    }

    const payload = {
      job_title: newJob.value.job_title,
      location: newJob.value.location,
      job_type: newJob.value.job_type,
      experience: newJob.value.experience,
      start_date: newJob.value.start_date,
      end_date: newJob.value.end_date,
      description_keywords: newJob.value.description_keywords || ""
    };

    const res = await fetch(`${API_BASE}/job`, {
      method: "POST",
      headers: { "Content-Type":"application/json", Authorization: `Bearer ${localStorage.getItem("token")}` },
      body: JSON.stringify(payload)
    });
    const data = await res.json().catch(()=>({}));
    if (!res.ok) {
      Swal.fire("Error", data.error || data.message || "Failed to create job", "error");
      creatingJob.value = false;
      return;
    }

    Swal.fire("Success", "Job created successfully!", "success");
    if (addJobModal) addJobModal.hide();
    await loadJobs();
    await loadRecruiterStats();
  } catch (err) {
    console.error("createJob error", err);
    Swal.fire("Error", "Server error while creating job", "error");
  } finally {
    creatingJob.value = false;
  }
}

// update job (edit)
async function updateJob() {
  updatingJob.value = true;
  try {
    if (!editJob.value || !editJob.value.job_id) {
      Swal.fire("Error", "Invalid job", "error");
      updatingJob.value = false;
      return;
    }

    // ensure experience is number
    editJob.value.experience = Number(editJob.value.experience || 0);

    const body = {
      job_title: editJob.value.job_title,
      location: editJob.value.location,
      job_type: editJob.value.job_type,
      experience: editJob.value.experience,
      start_date: editJob.value.start_date,
      end_date: editJob.value.end_date,
      description: editJob.value.description
    };

    const res = await fetch(`${API_BASE}/job/${editJob.value.job_id}`, {
      method: "PUT",
      headers: { "Content-Type":"application/json", Authorization: `Bearer ${localStorage.getItem("token")}` },
      body: JSON.stringify(body)
    });
    const data = await res.json().catch(()=>({}));
    if (!res.ok) {
      Swal.fire("Error", data.message || "Failed to update job", "error");
      updatingJob.value = false;
      return;
    }

    Swal.fire("Saved", "Job updated", "success");
    if (editJobModal) editJobModal.hide();
    await loadJobs();
    await loadRecruiterStats();
  } catch (err) {
    console.error("updateJob error", err);
    Swal.fire("Error", "Server error while updating job", "error");
  } finally {
    updatingJob.value = false;
  }
}

// applicants
const applicantsModalComponent = ref(null);
const viewApplicants = (job) => {
  if (applicantsModalComponent.value && applicantsModalComponent.value.openApplicantsModal) {
    applicantsModalComponent.value.openApplicantsModal(job);
  } else {
    // fallback: open applicants modal element if present
    // (kept intentionally empty as original ApplicantsModal component should handle UI)
  }
};

// edit job preview
const editJobPreviewHtml = computed(() => {
  try { return marked.parse(String(editJob.value.description || "")); } catch (e) { return "<pre>Invalid markdown</pre>"; }
});

// Full description job (modal)
function openFullDescription(job) {
  fullDescriptionJob.value = job;
  nextTick(() => { if (fullDescModalInstance) fullDescModalInstance.show(); });
}

// helper to clear search
function clearSearch() { searchQuery.value = ""; debouncedFilter(); currentPage.value = 1; }

// avatar using job title initials
function getInitialsFromTitle(title) {
  if (!title) return "JD";
  const words = title.split(/\s+/).filter(Boolean);
  if (words.length === 1) {
    const w = words[0];
    return (w[0] || "J").toUpperCase() + (w[1] || "").toUpperCase();
  }
  return ((words[0][0] || "") + (words[1][0] || "")).toUpperCase();
}
function generateJobAvatar(title) {
  const initials = getInitialsFromTitle(title);
  // using ui-avatars service which needs no API key; lightweight fallback
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&background=3864f2&color=fff&rounded=true&font-size=0.45`;
}

// expose for template
const getShortDescription = (job) => renderExcerpt(job.description);



</script>

<style scoped>
/* Layout */
.rec-dashboard { background: linear-gradient(135deg, #eef4ff, #f5f8ff); min-height: 100vh; padding-bottom: 40px; }

/* Stats row */
.stats-card {
  border-radius: 1.1rem;
  background: linear-gradient(135deg, #ffffff, #edf2ff);
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.12);
  border: 1px solid rgba(148, 163, 184, 0.2);
  min-height: 120px;
  padding: 20px 22px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

/* Hover effect */
.stats-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.22);
}

/* Icon bubble */
.stats-icon-wrapper {
  width: 46px;
  height: 46px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 20% 20%, #0d6efd, #2563eb);
  color: #fff;
  font-size: 1.25rem;
}

/* Text styling */
.stats-label {
  font-size: 0.8rem;
  opacity: 0.65;
  font-weight: 500;
}

.stats-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0d1b3d;
  margin-top: 2px;
}

/* Horizontal layout inside card */
.stats-card .stats-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-card {
    min-height: 105px;
    padding: 16px 18px;
  }

  .stats-icon-wrapper {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
}

/* Search input */
.search-input .form-control { height: 52px; border-radius: 999px; }
.search-input .input-group-text { border-radius: 999px 0 0 999px; border-right: none; padding-left: 14px; padding-right: 14px; }
.search-input .btn { margin-right: 6px; }

/* Job card */
.job-card { border-radius: 14px; transition: transform .22s cubic-bezier(.2,.9,.3,1), box-shadow .22s; display:flex; flex-direction:column; padding: 16px; background: linear-gradient(180deg,#ffffff,#fbfdff); border:1px solid rgba(10,30,80,0.04); }
.job-card:hover { transform: translateY(-8px); box-shadow: 0 26px 50px rgba(11, 42, 84, 0.10); }
.job-title { font-size: 1.05rem; margin-bottom: 0; }
.company-name { color: #0d6efd; font-weight: 600; }

/* Avatar */
.job-avatar {
  width:48px; height:48px; border-radius:12px; overflow:hidden; flex-shrink:0; background:#eef6ff; display:flex; align-items:center; justify-content:center;
}
.job-avatar img { width:100%; height:100%; object-fit:cover; display:block; }

/* job-desc */
.job-desc p { margin: 0; }

/* small pill badge */
.small-pill { font-size: 0.75rem; padding: 4px 8px; border-radius: 999px; }

/* Buttons unified modern */
.action-btn {
  transition: transform .12s ease, box-shadow .12s ease;
}
.action-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 18px rgba(11,42,84,0.08); }

/* form inputs in modals */
.modal .form-control, .modal .form-select { border-radius: 12px; padding: 10px 12px; }

/* preview */
.preview-box { min-height: 120px; background: #fff; border: 1px solid rgba(15,23,42,0.04); border-radius: 8px; overflow:auto; }

/* responsive */
@media (max-width: 768px) {
  .stats-row { justify-content: center; }
  .stats-card { min-width: 140px; }
  .job-avatar { width:44px; height:44px; border-radius:10px; }
}

/* pill & badge polish */
.badge.bg-light { background-color: #f6fbff; color: #0b63b7; border: 1px solid rgba(11,99,183,0.05); }

/* small helpers */
.form-label { font-weight:600; font-size:0.9rem; }
</style>
