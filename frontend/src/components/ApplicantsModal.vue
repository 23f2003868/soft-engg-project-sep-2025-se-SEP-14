<template>
  <div>
    <!-- Main Applicants Modal (hidden initially) -->
    <div
      class="modal fade"
      ref="modalRoot"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
      :aria-labelledby="'applicants-modal-title'"
    >
      <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
        <div class="modal-content rounded-4 shadow-lg">

          <!-- Header -->
          <div class="modal-header bg-primary text-white rounded-top-4">
            <div class="d-flex flex-column">
              <h5 id="applicants-modal-title" class="modal-title fw-bold">
                Applicants — <span class="text-white-50 fw-normal">{{ activeJob?.job_title || 'Loading...' }}</span>
              </h5>
              <small class="text-white-50">{{ activeJob?.location || '' }}</small>
            </div>
            <button type="button" class="btn btn-close btn-close-white" @click="hideModal" aria-label="Close"></button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <!-- Controls -->
            <div class="row g-2 align-items-center mb-3">
              <div class="col-md-4">
                <input
                  v-model="searchQuery"
                  @input="debouncedFilter"
                  class="form-control form-control-sm shadow-sm"
                  placeholder="Search candidate (name / email)..."
                  aria-label="Search applicants"
                />
              </div>

              <div class="col-md-3">
                <select v-model="statusFilter" class="form-select form-select-sm shadow-sm" aria-label="Filter by status">
                  <option value="ALL">All Statuses</option>
                  <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>

              <div class="col-md-3">
                <select v-model="sortOption" class="form-select form-select-sm shadow-sm" aria-label="Sort applicants">
                  <option value="NEWEST">Newest</option>
                  <option value="SCORE_DESC">Score (High → Low)</option>
                  <option value="SCORE_ASC">Score (Low → High)</option>
                </select>
              </div>

              <div class="col-md-2 d-flex gap-2 justify-content-end">
                <button class="btn btn-outline-secondary btn-sm" :disabled="loading" @click="downloadCSV" aria-label="Export CSV">
                  <i class="bi bi-download me-1"></i> Export
                </button>

                <button class="btn btn-primary btn-sm" :disabled="loading" @click="refresh" aria-label="Refresh list">
                  <i class="bi bi-arrow-clockwise me-1"></i> Refresh
                </button>
              </div>
            </div>

            <!-- Table -->
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0 small">
                <thead class="table-light">
                  <tr>
                    <th scope="col">Candidate</th>
                    <th scope="col">Email</th>
                    <th scope="col">Education</th>
                    <th scope="col" class="text-center">Score</th>
                    <th scope="col">Status</th>
                    <th scope="col">Applied On</th>
                    <th scope="col" class="text-center">Actions</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-if="loading">
                    <td colspan="7" class="text-center py-4">
                      <div class="spinner-border text-primary" role="status" aria-hidden="true"></div>
                      <div class="small text-muted mt-2">Loading applicants...</div>
                    </td>
                  </tr>

                  <tr v-for="a in paginatedApplicants" :key="a.candidate_job_request_id">
                    <td>
                      <div class="d-flex align-items-center">
                        <img :src="generateAvatar(a.candidate_name)" class="avatar me-2" alt="avatar" />
                        <div>
                          <div class="fw-semibold">{{ a.candidate_name }}</div>
                          <div class="small text-muted">{{ a.job_title }}</div>
                        </div>
                      </div>
                    </td>

                    <td class="text-muted">{{ a.email || '—' }}</td>
                    <td class="text-muted">{{ a.education || '—' }}</td>
                    <td class="text-center">
                      <span class="badge bg-info text-dark">{{ a.test_score ?? '—' }}</span>
                    </td>

                    <td>
                      <span :class="['badge', 'status-badge', 'text-uppercase', statusColorClass(a.status)]">{{ a.status }}</span>
                    </td>

                    <td class="text-muted">{{ a.applied_on || '—' }}</td>

                    <td class="text-center">
                      <div class="btn-group btn-group-sm" role="group" aria-label="Applicant actions">
                        <button class="btn btn-outline-primary" @click="openDetails(a)" title="View details">
                          <i class="bi bi-eye"></i>
                        </button>

                        <button class="btn btn-outline-success" @click="updateStatus(a, 'SHORTLISTED')" title="Shortlist">
                          <i class="bi bi-check2-circle"></i>
                        </button>

                        <button class="btn btn-outline-danger" @click="updateStatus(a, 'REJECTED')" title="Reject">
                          <i class="bi bi-x-circle"></i>
                        </button>
                      </div>
                    </td>
                  </tr>

                  <tr v-if="!loading && !paginatedApplicants.length">
                    <td colspan="7" class="text-center py-4 text-muted">
                      No applicants found.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination & info -->
            <div class="d-flex justify-content-between align-items-center mt-3">
              <div class="small text-muted">
                Showing {{ filteredApplicants.length }} applicants
              </div>

              <div class="d-flex align-items-center gap-2">
                <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage === 1" @click="currentPage--">Prev</button>
                <span class="small">Page {{ currentPage }} / {{ totalPages }}</span>
                <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage >= totalPages" @click="currentPage++">Next</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Candidate Details Modal -->
    <div class="modal fade" ref="detailsModalRoot" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4">
          <div class="modal-header border-0">
            <h5 class="modal-title fw-semibold">{{ selectedCandidate?.candidate_name || 'Candidate' }}</h5>
            <button type="button" class="btn btn-close" @click="hideDetailsModal" aria-label="Close"></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-4 text-center">
                <img :src="generateAvatar(selectedCandidate?.candidate_name)" class="avatar-large mb-2" alt="avatar" />
                <div class="small text-muted">{{ selectedCandidate?.status }}</div>
              </div>

              <div class="col-md-8">
                <table class="table table-sm mb-3">
                  <tbody>
                    <tr><th class="w-25">Email</th><td>{{ selectedCandidate?.email || '—' }}</td></tr>
                    <tr><th>Education</th><td>{{ selectedCandidate?.education || '—' }}</td></tr>
                    <tr><th>Age</th><td>{{ selectedCandidate?.age ?? '—' }}</td></tr>
                    <tr><th>Score</th><td>{{ selectedCandidate?.test_score ?? '—' }}</td></tr>
                    <tr><th>Applied On</th><td>{{ selectedCandidate?.applied_on || '—' }}</td></tr>
                  </tbody>
                </table>

                <div class="d-flex gap-2">
                  <button class="btn btn-success" @click="updateStatus(selectedCandidate, 'SHORTLISTED')">Shortlist</button>
                  <button class="btn btn-danger" @click="updateStatus(selectedCandidate, 'REJECTED')">Reject</button>
                  <button class="btn btn-info text-white" @click="updateStatus(selectedCandidate, 'INTERVIEWED')">Mark Interviewed</button>

                  <a
                    v-if="selectedCandidate?.resume_url"
                    :href="resumeDownloadLink(selectedCandidate.resume_url)"
                    class="btn btn-outline-primary ms-auto"
                    target="_blank"
                    rel="noopener"
                  >
                    <i class="bi bi-cloud-arrow-down"></i> Resume
                  </a>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* ApplicantsModal.vue
   - Exposes openApplicantsModal(job) for parent (defineExpose)
   - Keeps the same backend endpoints (recruiter/applications & candidate-job-request/:id)
   - Uses Bootstrap modal via refs
*/

import { ref, computed, watch, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import Swal from 'sweetalert2';
import debounce from 'lodash/debounce'; // if lodash not available, fallback included below

// Environment / API (matches your dashboard)
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000/api";
const BASE_URL = API_BASE.replace('/api', '');
const token = localStorage.getItem('token') || '';

// STATE
const modalRoot = ref(null);
const detailsModalRoot = ref(null);
let bsModal = null;
let bsDetailsModal = null;

const activeJob = ref(null);
const applicants = ref([]);
const loading = ref(false);
const error = ref(null);

const searchQuery = ref('');
const statusFilter = ref('ALL');
const sortOption = ref('NEWEST');

const pageSize = 8;
const currentPage = ref(1);

const selectedCandidate = ref(null);

// statuses to show in filter (kept consistent with backend)
const statuses = ['APPLIED', 'SHORTLISTED', 'INTERVIEWED', 'HIRED', 'REJECTED'];

/* -------------------
   API: load applicants
   ------------------- */
const loadApplicants = async (jobId) => {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API_BASE}/recruiter/applications?job_id=${jobId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || 'Failed to load applicants');
    }
    const data = await res.json();
    applicants.value = data.applications || [];
    currentPage.value = 1;
  } catch (err) {
    applicants.value = [];
    error.value = err.message || 'Server error';
    Swal.fire('Error', error.value, 'error');
  } finally {
    loading.value = false;
  }
};

/* ---------------
   Filtering & sort
   --------------- */
const filteredApplicants = computed(() => {
  let list = applicants.value ? [...applicants.value] : [];

  const q = (searchQuery.value || '').trim().toLowerCase();
  if (q) {
    list = list.filter(a =>
      (a.candidate_name || '').toLowerCase().includes(q) ||
      (a.email || '').toLowerCase().includes(q)
    );
  }

  if (statusFilter.value !== 'ALL') {
    list = list.filter(a => a.status === statusFilter.value);
  }

  if (sortOption.value === 'SCORE_DESC') {
    list.sort((x, y) => (y.test_score || 0) - (x.test_score || 0));
  } else if (sortOption.value === 'SCORE_ASC') {
    list.sort((x, y) => (x.test_score || 0) - (y.test_score || 0));
  } else {
    // NEWEST - by applied_on desc
    list.sort((a, b) => {
      const da = a.applied_on ? new Date(a.applied_on) : 0;
      const db = b.applied_on ? new Date(b.applied_on) : 0;
      return db - da;
    });
  }

  return list;
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredApplicants.value.length / pageSize)));

const paginatedApplicants = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredApplicants.value.slice(start, start + pageSize);
});

/* ------------------------
   Actions: status / details
   ------------------------ */
const updateStatus = async (candidate, status) => {
  if (!candidate || !candidate.candidate_job_request_id) return;
  try {
    const res = await fetch(`${API_BASE}/candidate-job-request/${candidate.candidate_job_request_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ status })
    });
    if (!res.ok) {
      const d = await res.json().catch(()=>null);
      throw new Error(d?.message || d?.error || 'Failed to update');
    }
    Swal.fire('Updated', `Status set to ${status}`, 'success');
    // reload list
    await loadApplicants(activeJob.value.job_id);
    // if a details modal open, close it
    hideDetailsModal();
  } catch (err) {
    Swal.fire('Error', err.message || 'Failed to update status', 'error');
  }
};

const openDetails = (candidate) => {
  selectedCandidate.value = candidate;
  // show details modal
  nextTick(() => {
    if (!bsDetailsModal) bsDetailsModal = new Modal(detailsModalRoot.value);
    bsDetailsModal.show();
  });
};

const hideDetailsModal = () => {
  if (bsDetailsModal) bsDetailsModal.hide();
  selectedCandidate.value = null;
};

/* --------------------------
   Utility: resume download link
   -------------------------- */
const resumeDownloadLink = (resumePath) => {
  // If the candidate.resume_url is a full path, return as-is; otherwise build using BASE_URL/uploads
  if (!resumePath) return '#';
  if (resumePath.startsWith('http') || resumePath.startsWith('/')) {
    // if starts with /uploads/filename or full url, try to return full url
    if (resumePath.startsWith('/')) return `${BASE_URL}${resumePath}`;
    return resumePath;
  }
  return `${BASE_URL}/uploads/${encodeURIComponent(resumePath)}`;
};

/* --------------------------
   CSV export
   -------------------------- */
const sanitize = (v) => {
  if (v === null || v === undefined) return '';
  return String(v).replace(/"/g, '""');
};

const downloadCSV = () => {
  const rows = filteredApplicants.value.map(a => ({
    Name: a.candidate_name || '',
    Email: a.email || '',
    Education: a.education || '',
    Score: a.test_score ?? '',
    Status: a.status || '',
    AppliedOn: a.applied_on || ''
  }));
  if (!rows.length) {
    Swal.fire('No data', 'No applicants to export', 'info');
    return;
  }

  const header = Object.keys(rows[0]).join(',');
  const csv = [
    header,
    ...rows.map(r => Object.values(r).map(v => `"${sanitize(v)}"`).join(','))
  ].join('\n');

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `applicants_job_${activeJob.value?.job_id || 'list'}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
};

/* --------------------------
   Modal helpers and expose
   -------------------------- */
const showModal = async (job) => {
  activeJob.value = job || null;
  if (!job) return;
  // load applicants for job
  await loadApplicants(job.job_id);
  // initialize bootstrap modal if not
  await nextTick();
  if (!bsModal) bsModal = new Modal(modalRoot.value);
  bsModal.show();
};

const hideModal = () => {
  if (bsModal) bsModal.hide();
  activeJob.value = null;
  applicants.value = [];
  currentPage.value = 1;
};

/* Expose method for parent to call */
defineExpose({ openApplicantsModal: showModal });

/* init details modal on mount when DOM ready */
setTimeout(() => {
  if (modalRoot.value && !bsModal) bsModal = new Modal(modalRoot.value);
  if (detailsModalRoot.value && !bsDetailsModal) bsDetailsModal = new Modal(detailsModalRoot.value);
}, 100);

/* refresh button */
const refresh = async () => {
  if (!activeJob.value) return;
  await loadApplicants(activeJob.value.job_id);
};

/* Debounce search to avoid heavy calls (client-only filter - debounce just improves UX) */
let lodashDebounce;
try {
  // if lodash is bundled in your project this will use it
  lodashDebounce = debounce;
} catch (e) {
  // fallback simple debounce
  lodashDebounce = (fn, wait = 300) => {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), wait);
    };
  };
}
const debouncedFilter = lodashDebounce(() => { currentPage.value = 1; }, 250);

/* small helper for avatars */
const generateAvatar = (name) =>
  `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'U')}&background=0D8ABC&color=fff&rounded=true`;

/* computed for filtered length & pages watchers */
watch([searchQuery, statusFilter, sortOption], () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.modal-content { border: none; }
.modal-header { gap: 0.5rem; align-items: center; }

.avatar {
  width: 40px; height: 40px; border-radius: 50%; object-fit: cover;
}
.avatar-large { width: 110px; height: 110px; border-radius: 12px; object-fit: cover; }

.status-badge {
  padding: 0.45rem 0.6rem;
  border-radius: 8px;
  font-size: 0.72rem;
}

/* Colors for statuses */
.status-badge.bg-APPLIED { background: #e9ecef; color: #333; }
.status-badge.bg-SHORTLISTED { background: #dff7e3; color: #0b6623; }
.status-badge.bg-INTERVIEWED { background: #e7f5ff; color: #055160; }
.status-badge.bg-HIRED { background: #f0f7ff; color: #0b3d91; }
.status-badge.bg-REJECTED { background: #fff0f0; color: #8b0000; }

/* small responsive tweaks */
@media (max-width: 720px) {
  .modal-dialog { max-width: 95% !important; }
  .avatar-large { width: 96px; height: 96px; }
}
</style>
