<template>
  <div>

    <!-- MAIN MODAL -->
    <div class="modal fade"
         ref="modalRoot"
         tabindex="-1"
         aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content rounded-4 shadow-lg">

          <!-- HEADER -->
          <div class="modal-header bg-primary text-white rounded-top-4">
            <div>
              <h5 class="modal-title fw-bold">
                Applicants — 
                <span class="text-white-50">{{ activeJob?.job_title }}</span>
              </h5>
              <small class="text-white-50">{{ activeJob?.location }}</small>
            </div>
            <button class="btn btn-close btn-close-white"
                    @click.stop="hideModal"></button>
          </div>

          <!-- BODY -->
          <div class="modal-body">

            <!-- FILTERS -->
            <div class="row g-2 mb-3">
              <div class="col-md-4">
                <input v-model="searchQuery"
                       class="form-control form-control-sm"
                       placeholder="Search (name/email)..." />
              </div>

              <div class="col-md-3">
                <select v-model="statusFilter"
                        class="form-select form-select-sm">
                  <option value="ALL">All Statuses</option>
                  <option v-for="s in statuses" :key="s" :value="s">
                    {{ s }}
                  </option>
                </select>
              </div>

              <div class="col-md-3">
                <select v-model="sortOption"
                        class="form-select form-select-sm">
                  <option value="NEWEST">Newest First</option>
                  <option value="SCORE_DESC">Score High → Low</option>
                  <option value="SCORE_ASC">Score Low → High</option>
                </select>
              </div>

              <div class="col-md-2 d-flex gap-2 justify-content-end">
                <button class="btn btn-outline-secondary btn-sm"
                        @click="downloadCSV"
                        :disabled="loading">
                  <i class="bi bi-download me-1"></i> Export
                </button>

                <button class="btn btn-primary btn-sm"
                        @click="refresh"
                        :disabled="loading">
                  <i class="bi bi-arrow-clockwise me-1"></i> Refresh
                </button>
              </div>
            </div>

            <!-- TABLE -->
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0 small">
                <thead class="table-light">
                  <tr>
                    <th>Candidate</th>
                    <th>Email</th>
                    <th>Education</th>
                    <th class="text-center">Score</th>
                    <th>Status</th>
                    <th>Applied On</th>
                    <th class="text-center">Actions</th>
                  </tr>
                </thead>

                <tbody>

                  <!-- SPINNER -->
                  <tr v-if="loading">
                    <td colspan="7" class="text-center py-4">
                      <div class="spinner-border text-primary"></div>
                      <div class="small text-muted mt-2">
                        Loading applicants...
                      </div>
                    </td>
                  </tr>

                  <!-- EMPTY -->
                  <tr v-else-if="paginatedApplicants.length === 0">
                    <td colspan="7" class="text-center py-4 text-muted">
                      No applicants found.
                    </td>
                  </tr>

                  <!-- ROWS -->
                  <tr v-for="a in paginatedApplicants"
                      :key="a.candidate_job_request_id">

                    <td>
                      <div class="d-flex align-items-center">
                        <img :src="generateAvatar(a.candidate_name)"
                             class="avatar me-2" />
                        <div class="fw-semibold">{{ a.candidate_name }}</div>
                      </div>
                    </td>

                    <td class="text-muted">{{ a.email }}</td>

                    <td class="text-muted">{{ a.education }}</td>

                    <td class="text-center">
                      <span class="badge bg-info text-dark">
                        {{ a.test_score ?? "—" }}
                      </span>
                    </td>

                    <td>
                      <span class="badge text-uppercase"
                            :class="statusColorClass(a.status)">
                        {{ a.status }}
                      </span>
                    </td>

                    <td class="text-muted">{{ a.applied_on }}</td>

                    <td class="text-center">
                      <div class="btn-group btn-group-sm">

                        <button class="btn btn-outline-primary"
                                @click.stop="openDetails(a)">
                          <i class="bi bi-eye"></i>
                        </button>

                        <button class="btn btn-outline-success"
                                @click.stop="updateStatus(a, 'SHORTLISTED')">
                          <i class="bi bi-check2-circle"></i>
                        </button>

                        <button class="btn btn-outline-danger"
                                @click.stop="updateStatus(a, 'REJECTED')">
                          <i class="bi bi-x-circle"></i>
                        </button>

                      </div>
                    </td>

                  </tr>
                </tbody>
              </table>
            </div>

            <!-- PAGINATION -->
            <div class="d-flex justify-content-between mt-3">
              <small class="text-muted">
                {{ filteredApplicants.length }} applicants
              </small>

              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-secondary"
                        :disabled="currentPage === 1"
                        @click="currentPage--">Prev</button>

                <span class="small">
                  Page {{ currentPage }} / {{ totalPages }}
                </span>

                <button class="btn btn-sm btn-outline-secondary"
                        :disabled="currentPage >= totalPages"
                        @click="currentPage++">Next</button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>


    <!-- DETAILS MODAL -->
    <div class="modal fade"
         ref="detailsModalRoot"
         tabindex="-1"
         aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title fw-semibold">
              {{ selectedCandidate?.candidate_name }}
            </h5>
            <button class="btn btn-close" @click.stop="hideDetailsModal"></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">

              <div class="col-md-4 text-center">
                <img :src="generateAvatar(selectedCandidate?.candidate_name)"
                     class="avatar-large mb-2" />
                <div class="small text-muted">
                  {{ selectedCandidate?.status }}
                </div>
              </div>

              <div class="col-md-8">
                <table class="table table-sm">
                  <tbody>
                    <tr><th>Email</th><td>{{ selectedCandidate?.email }}</td></tr>
                    <tr><th>Education</th><td>{{ selectedCandidate?.education }}</td></tr>
                    <tr><th>Age</th><td>{{ selectedCandidate?.age }}</td></tr>
                    <tr><th>Score</th><td>{{ selectedCandidate?.test_score }}</td></tr>
                    <tr><th>Applied On</th><td>{{ selectedCandidate?.applied_on }}</td></tr>
                  </tbody>
                </table>

                <a v-if="selectedCandidate?.resume_url"
                   :href="resumeDownloadLink(selectedCandidate.resume_url)"
                   target="_blank"
                   class="btn btn-outline-primary">
                  <i class="bi bi-cloud-arrow-down"></i> Resume
                </a>

              </div>

            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
/* ----------------------------------------------------------------------
   FIXED FULL VERSION — SAFE STATUS UPDATE + NO EVENT BUBBLES
---------------------------------------------------------------------- */

import { ref, computed, nextTick } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000/api";
const BASE_URL = API_BASE.replace("/api", "");
const token = localStorage.getItem("token");

/* STATE */
const modalRoot = ref(null);
const detailsModalRoot = ref(null);
let bsModal = null;
let bsDetailsModal = null;

const activeJob = ref(null);
const applicants = ref([]);
const loading = ref(false);

const searchQuery = ref("");
const statusFilter = ref("ALL");
const sortOption = ref("NEWEST");
const currentPage = ref(1);
const selectedCandidate = ref(null);
const pageSize = 8;

const statuses = ["APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED", "INTERVIEWED", "HIRED", "REJECTED"];

/* LOAD APPLICANTS */
const loadApplicants = async (jobId) => {
  loading.value = true;

  try {
    const res = await fetch(`${API_BASE}/recruiter/applications?job_id=${jobId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();
    applicants.value = data.applications || [];

  } catch (e) {
    Swal.fire("Error", "Failed to load applicants", "error");
    applicants.value = [];
  }

  loading.value = false;
};


/* FILTERS */
const filteredApplicants = computed(() => {
  let list = [...applicants.value];

  const q = searchQuery.value.toLowerCase();

  if (q) {
    list = list.filter(a =>
      a.candidate_name?.toLowerCase().includes(q) ||
      a.email?.toLowerCase().includes(q)
    );
  }

  if (statusFilter.value !== "ALL") {
    list = list.filter(a => a.status === statusFilter.value);
  }

  if (sortOption.value === "SCORE_DESC") {
    list.sort((a, b) => (b.test_score ?? 0) - (a.test_score ?? 0));
  } else if (sortOption.value === "SCORE_ASC") {
    list.sort((a, b) => (a.test_score ?? 0) - (b.test_score ?? 0));
  } else {
    list.sort((a, b) => new Date(b.applied_on) - new Date(a.applied_on));
  }

  return list;
});

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredApplicants.value.length / pageSize))
);

const paginatedApplicants = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredApplicants.value.slice(start, start + pageSize);
});


/* STATUS COLOR */
const statusColorClass = (status) =>
  ({
    APPLIED: "bg-secondary",
    SHORTLISTED: "bg-warning",
    INTERVIEW_SCHEDULED: "bg-primary",
    INTERVIEWED: "bg-info",
    HIRED: "bg-success",
    REJECTED: "bg-danger"
  }[status] || "bg-light");


/* UPDATE STATUS — FIXED */
const updateStatus = async (user, status) => {
  if (!status || !status.trim()) {
    console.warn("Ignored empty status update.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/candidate-job-request/${user.candidate_job_request_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ status })
    });

    const d = await res.json();

    if (!res.ok || !d.success) {
      Swal.fire("Error", d.message || "Failed to update status", "error");
      return;
    }

    Swal.fire("Updated!", `Status changed to ${status}`, "success");
    await loadApplicants(activeJob.value.job_id);

  } catch (e) {
    Swal.fire("Error", "Server error while updating", "error");
  }
};


/* DETAILS MODAL */
const openDetails = (user) => {
  selectedCandidate.value = user;

  nextTick(() => {
    if (!bsDetailsModal) {
      bsDetailsModal = new Modal(detailsModalRoot.value, {
        backdrop: "static",
        keyboard: false
      });
    }
    bsDetailsModal.show();
  });
};


const hideDetailsModal = () => {
  if (bsDetailsModal) bsDetailsModal.hide();
  selectedCandidate.value = null;
};


/* RESUME LINK */
const resumeDownloadLink = (path) => {
  if (!path) return "#";
  if (path.startsWith("http")) return path;
  if (path.startsWith("/")) return BASE_URL + path;
  return `${BASE_URL}/uploads/${path}`;
};


/* CSV EXPORT */
const sanitize = (v) => String(v ?? "").replace(/"/g, '""');

const downloadCSV = () => {
  const rows = filteredApplicants.value.map(a => ({
    Name: a.candidate_name,
    Email: a.email,
    Education: a.education,
    Score: a.test_score,
    Status: a.status,
    AppliedOn: a.applied_on
  }));

  if (!rows.length) {
    Swal.fire("No Data", "No applicants to export.", "info");
    return;
  }

  const header = Object.keys(rows[0]).join(",");
  const csv = [
    header,
    ...rows.map(r => Object.values(r).map(v => `"${sanitize(v)}"`).join(",")),
  ].join("\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `applicants_${activeJob.value.job_id}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
};


/* AVATAR */
const generateAvatar = (name) =>
  `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "User")}&background=0D8ABC&color=fff&rounded=true`;


/* MODAL */
const showModal = async (job) => {
  activeJob.value = job;
  await loadApplicants(job.job_id);

  nextTick(() => {
    if (!bsModal) {
      bsModal = new Modal(modalRoot.value, {
        backdrop: "static",
        keyboard: false
      });
    }
    bsModal.show();
  });
};


const hideModal = () => {
  if (bsModal) bsModal.hide();
  applicants.value = [];
  activeJob.value = null;
};

const refresh = () => {
  if (activeJob.value) loadApplicants(activeJob.value.job_id);
};

defineExpose({ openApplicantsModal: showModal });
</script>


<style scoped>
.modal-content { border: none; }

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-large {
  width: 110px;
  height: 110px;
  border-radius: 12px;
  object-fit: cover;
}

@media (max-width: 720px) {
  .modal-dialog { max-width: 95% !important; }
  .avatar-large { width: 96px; height: 96px; }
}
</style>
