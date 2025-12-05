<template>
  <div>
    <Topbar />

    <div class="kanban-wrapper bg-light min-vh-100 py-5 px-3">
      <div class="text-center mb-4">
        <h2 class="fw-bold text-primary">Smart Candidate Tracker</h2>
        <p class="text-muted">Drag & drop candidates through the hiring pipeline</p>
      </div>

      <div class="d-flex justify-content-center mb-3">
        <select v-model="selectedJobId" @change="onJobChange" class="form-select w-75 w-md-50 rounded-pill px-3 py-2 shadow-sm">
          <option value="">Select Job Title</option>
          <option v-for="job in jobs" :key="job.job_id" :value="job.job_id">{{ job.job_title }}</option>
        </select>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-3 w-75 mx-auto">
        <input v-model="searchQuery" @input="applyFilters" placeholder="Search candidate or job title..." class="form-control w-50 rounded-pill px-3 py-2" />

        <div class="d-flex gap-2 align-items-center">
          <small class="text-muted me-2">{{ total }} candidates</small>

          <button class="btn btn-sm btn-outline-secondary" :disabled="page===1" @click="changePage(page-1)">Prev</button>
          <span class="small">Page {{ page }} / {{ totalPages }}</span>
          <button class="btn btn-sm btn-outline-secondary" :disabled="page>=totalPages" @click="changePage(page+1)">Next</button>

          <select v-model.number="perPage" @change="changePerPage" class="form-select form-select-sm ms-2">
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="40">40</option>
          </select>
        </div>
      </div>

      <div class="row g-4 justify-content-center">
        <div v-for="(stage, si) in stages" :key="stage.name" class="col-12 col-md-6 col-lg-2 d-flex flex-column">
          <div class="card border-0 shadow-sm flex-grow-1">
            <div class="card-header fw-bold text-center text-white" :style="{ backgroundColor: stage.color }">
              {{ stage.label }}
            </div>

            <div class="card-body p-3 overflow-auto" style="max-height: 65vh;" :data-stage-index="si">
              <draggable
                :list="stage.candidates"
                :group="{ name: 'pipeline', pull: true, put: true }"
                item-key="id"
                @end="onDragEnd"
              >
                <template #item="{ element, index }">
                  <div
                    class="candidate-wrapper"
                    :data-cjr-id="element.id"
                    :data-index="index"
                    style="width:100%;"
                  >
                    <div
                      v-show="isVisible(element)"
                      class="candidate-card border rounded-3 p-3 mb-3 bg-white shadow-sm"
                    >
                      <h6 class="fw-semibold text-dark mb-1">
                        <i class="bi bi-person-circle me-2 text-primary"></i> {{ element.name }}
                      </h6>
                      <p class="text-muted small mb-1"><i class="bi bi-briefcase me-1"></i> {{ element.jobTitle }}</p>
                      <p class="text-muted small mb-0"><i class="bi bi-envelope me-1"></i> {{ element.email }}</p>
                    </div>
                  </div>
                </template>
              </draggable>

              <p v-if="stage.candidates.filter(isVisible).length === 0" class="text-muted small text-center mt-3">No candidates</p>
            </div>
          </div>
        </div>
      </div>

      <SchedulingModal
        v-if="modalCjrId"
        :visible="showModal"
        :cjrId="modalCjrId"
        :candidateName="modalCandidateName"
        :apiBase="API_URL"
        :token="token"
        @scheduled="onScheduled"
        @cancel="onModalCancel"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import draggable from 'vuedraggable';
import Swal from 'sweetalert2'; 
import Topbar from "../components/RecruiterNavbar.vue"; 
import SchedulingModal from './SchedulingModal.vue'; 

const API_URL = "http://127.0.0.1:5000/api";
const token = localStorage.getItem("token") || "";

/* state */
const jobs = ref([]);
const selectedJobId = ref("");
const searchQuery = ref("");
const isConnected = ref(false); 

/* Pagination */
const page = ref(1);
const perPage = ref(20);
const total = ref(0);
const totalPages = ref(1);

/* Kanban stages */
const stages = reactive([
  { label: "Applied", name: "APPLIED", color: "#9BBDF9", candidates: [] },
  { label: "Shortlisted", name: "SHORTLISTED", color: "#7EC8E3", candidates: [] },
  { label: "Interview Scheduled", name: "INTERVIEW_SCHEDULED", color: "#F5D547", candidates: [] },
  { label: "Interviewed", name: "INTERVIEWED", color: "#FBC252", candidates: [] },
  { label: "Offered", name: "OFFERED", color: "#81C784", candidates: [] },
  { label: "Hired", name: "HIRED", color: "#4CAF50", candidates: [] },
  { label: "Rejected", name: "REJECTED", color: "#DE6262", candidates: [] }
]);

/* Modal state */
const showModal = ref(false);
const modalCjrId = ref(null);
const modalCandidateName = ref("");

/* Load recruiter jobs */
async function loadRecruiterJobs() {
  try {
    const res = await fetch(`${API_URL}/recruiter/jobs`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    const data = await res.json();
    jobs.value = data.jobs || [];
  } catch (e) {
    console.error("Failed loading jobs", e);
  }
}

/* Load candidates for selected job (paginated) */
async function loadCandidates() {
  if (!selectedJobId.value) return;
  try {
    const res = await fetch(`${API_URL}/recruiter/applications-paged?job_id=${selectedJobId.value}&page=${page.value}&per_page=${perPage.value}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    const data = await res.json();
    if (!data.success) {
      console.error("Failed to load applications:", data);
      return;
    }

    // reset stage arrays
    stages.forEach(s => (s.candidates = []));

    total.value = data.total || 0;
    totalPages.value = Math.max(1, Math.ceil(total.value / perPage.value));

    (data.applications || []).forEach(c => {
      const stage = stages.find(s => s.name === c.status) || stages[0];
      stage.candidates.push({
        id: c.candidate_job_request_id,
        name: c.candidate_name,
        email: c.email,
        jobTitle: c.job_title,
        raw: c
      });
    });
  } catch (e) {
    console.error("Error loading paged applications", e);
  }
}

/* events */
function onJobChange() {
  page.value = 1;
  loadCandidates();
}

function changePage(p) {
  if (p < 1) p = 1;
  if (p > totalPages.value) p = totalPages.value;
  page.value = p;
  loadCandidates();
}
function changePerPage() {
  page.value = 1;
  loadCandidates();
}

function applyFilters() {
  // client-side: v-show uses isVisible
}

const isVisible = (candidate) => {
  const q = searchQuery.value?.toLowerCase?.() || "";
  if (!q) return true;
  return candidate.name.toLowerCase().includes(q) || candidate.jobTitle.toLowerCase().includes(q) || candidate.email.toLowerCase().includes(q);
};

/* DRAG handling - robust */
async function onDragEnd(evt) {
  try {
    if (!evt || !evt.item) {
      loadCandidates();
      return;
    }

    let movedId = null;
    let movedName = null;

    // 1. Get movedId and movedName reliably from the draggable context
    try {
        const ctx = evt.item.__draggable_context || evt.item._underlying_vm_;
        const element = ctx && ctx.element ? ctx.element : ctx;
        if (element && element.id !== undefined) {
          movedId = String(element.id);
          movedName = element.name; // CAPTURE NAME HERE
        }
    } catch (e) {/* ignore */}
    
    // Fallback on DOM data attribute if context failed
    if (!movedId) {
        const wrapper = evt.item.closest('[data-cjr-id]');
        if (wrapper && wrapper.dataset && wrapper.dataset.cjrId) {
            movedId = String(wrapper.dataset.cjrId);
        }
    }

    if (!movedId) {
      loadCandidates();
      return;
    }

    // Determine destination stage index
    let stageIndex = null;
    try {
      const toEl = evt.to;
      if (toEl) {
        const parentWithIndex = toEl.closest("[data-stage-index]");
        if (parentWithIndex && parentWithIndex.dataset && parentWithIndex.dataset.stageIndex != null) {
          stageIndex = Number(parentWithIndex.dataset.stageIndex);
        }
      }
    } catch (err) {
      stageIndex = null;
    }

    if (stageIndex == null || isNaN(stageIndex)) {
      loadCandidates();
      return;
    }

    const destStatus = stages[stageIndex]?.name;
    if (!destStatus) {
      loadCandidates();
      return;
    }

    // FIX: If target is Interview Scheduled -> prepare modal state
    if (destStatus === "INTERVIEW_SCHEDULED") {
      
      // Check if Google is connected before proceeding to schedule
      if (!isConnected.value) {
        Swal.fire({
          icon: 'warning',
          title: 'Connection Required',
          text: 'Please connect your Google Calendar to schedule interviews.',
          confirmButtonText: 'OK',
        });
        loadCandidates();
        return;
      }
      
      // 1. Set data to MOUNT the modal component
      modalCjrId.value = movedId;
      modalCandidateName.value = movedName || "";
      
      // 2. Wait for VUE to mount the component in the DOM
      await nextTick();
      
      // 3. Tell the mounted component to SHOW the Bootstrap Modal (via prop)
      showModal.value = true;
      
      // 4. Now safely reset the Kanban UI list state (this causes drag undo)
      loadCandidates();
      
      return;
    }

    // Normal update -> PUT to backend
    const res = await fetch(`${API_URL}/candidate-job-request/${movedId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {})
      },
      body: JSON.stringify({ status: destStatus })
    });

    const data = await res.json().catch(()=>({}));
    if (!res.ok || !data.success) {
      Swal.fire({
          icon: 'error',
          title: 'Status Update Failed',
          text: data.message || data.error || "An unknown error occurred while updating the candidate status.",
          confirmButtonText: 'OK',
      });
    }

    // reload canonical
    loadCandidates();

  } catch (err) {
    console.error("Drag error:", err);
    loadCandidates();
  }
}

/* modal handlers */
function clearModalState() {
  showModal.value = false;
  modalCjrId.value = null;
  modalCandidateName.value = "";
}

function onModalCancel() {
  // Clear the state only after a small delay to allow Bootstrap hide animation to start
  setTimeout(() => {
    clearModalState();
  }, 100); 
}

function onScheduled(payload) {
  // After scheduling success
  // Clear modal and refresh data to show candidate in "Interview Scheduled" column
  setTimeout(() => {
    clearModalState();
    loadCandidates();
  }, 100);
}

async function connectGoogle() {
  try {
    // Step 1 — Get Google OAuth URL
    const res = await fetch(`${API_URL}/google-oauth-url`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    const data = await res.json();

    if (!data.success) {
      Swal.fire({
          icon: 'error',
          title: 'Configuration Error',
          text: 'Failed to retrieve Google OAuth URL. Check backend configuration.',
          confirmButtonText: 'OK',
      });
      return;
    }
    
    // Show a static alert indicating the user should complete the popup
    const swalInstance = Swal.fire({
      title: 'Google Authorization Required',
      icon: 'info',
      html: `
        <p class="text-muted mb-3">Please grant permission in the new window that just opened.</p>
        <p class="text-warning small">If you don't see a window, check your browser's popup blocker.</p>
      `,
      showConfirmButton: false, // Hide the initial button
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => {
        // Step 2 — Open Google Auth popup
        const popup = window.open(data.url, "_blank", "width=500,height=600");
        
        // Step 3 — Listen for authorization code
        const messageListener = async (event) => {
          // Security check: ensure event origin is expected
          if (event.origin !== "http://127.0.0.1:5000" && event.origin !== "http://localhost:5000") {
              return;
          }
          
          const code = event.data?.code;
          if (!code) return;
          
          // Remove listener immediately after receiving the code
          window.removeEventListener("message", messageListener);
          
          // Update Swal to show loading state while processing the code
          Swal.update({
              title: 'Processing Connection...',
              html: 'Please wait while we secure your authorization tokens.',
              icon: 'info',
              showCancelButton: false,
              showConfirmButton: false,
          });
          Swal.showLoading();

          // Step 4 — Send code to backend
          const res2 = await fetch(`${API_URL}/google-exchange-code`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              ...(token ? { Authorization: `Bearer ${token}` } : {})
            },
            body: JSON.stringify({ code })
          });

          const resp = await res2.json();
          
          // Step 5: Handle success or failure
          if (resp.success) {
            isConnected.value = true; // Update state
            
            // Success: Update Swal message and CLOSE it
            Swal.fire({
                icon: 'success',
                title: 'Connection Successful!',
                text: 'Google Calendar is now connected for scheduling.',
                timer: 3000,
                showConfirmButton: false
            });
            
          } else {
            // Failure: Update Swal message and let the user click OK to retry/close
            Swal.hideLoading();
            Swal.update({
                icon: 'error',
                title: 'Connection Failed',
                html: resp.message || "An unexpected error occurred during token exchange. You may retry.",
                showConfirmButton: true,
                confirmButtonText: 'OK / Retry',
            });
          }
        };
        
        window.addEventListener("message", messageListener);
      }
    });

  } catch (err) {
    console.error(err);
    Swal.fire({
        icon: 'error',
        title: 'Connection Error',
        text: 'An unexpected error occurred while initiating the Google connection flow.',
        confirmButtonText: 'OK',
    });
  }
}


async function checkGoogleConnection() {
  try {
    const res = await fetch(`${API_URL}/google-status`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    const data = await res.json();

    return data.connected === true;
  } catch {
    return false;
  }
}



/* lifecycle */
onMounted(async () => {
  loadRecruiterJobs();

  const isConnectedNow = await checkGoogleConnection();
  isConnected.value = isConnectedNow; // Set reactive state

  if (!isConnectedNow) {
    // Display SweetAlert prompt if not connected
    Swal.fire({
      title: "Google Calendar Not Connected",
      icon: "info",
      html: `
        <p class="text-muted mb-4">You need to connect your Google account to automatically schedule interviews and create Google Meet links.</p>
        <button id="connectBtn" class="btn btn-danger px-4 py-2 shadow-sm">
          <i class="bi bi-google me-2"></i> Connect with Google
        </button>
      `,
      showConfirmButton: false,
      allowOutsideClick: false,
      allowEscapeKey: false,
      customClass: {
        confirmButton: 'btn btn-primary' // Custom class for buttons if shown
      },
      didOpen: () => {
        // Attach listener to the button inside the SweetAlert
        document.getElementById("connectBtn").onclick = async () => {
          // Instead of closing, call connectGoogle which handles the loading state update
          await connectGoogle();
        };
      }
    });
  }
});

</script>

<style scoped>
.kanban-wrapper {
  background: linear-gradient(180deg, #f9fafc 0%, #eef3f8 100%);
}
.card { border-radius: 16px; transition: transform 0.2s ease, box-shadow 0.2s ease; }
.card:hover { transform: translateY(-3px); box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.card-header { border-top-left-radius: 16px !important; border-top-right-radius: 16px !important; font-size: 1rem; letter-spacing: 0.5px; }
.candidate-card { transition: all 0.2s ease-in-out; cursor: grab; }
.candidate-card:hover { background-color: #f8faff; transform: scale(1.02); border-color: #b3d4fc; }
/* Ensure the custom button styles look good */
.btn-primary { background-color: #4285F4; border-color: #4285F4; }
.btn-primary:hover { background-color: #357ae8; border-color: #357ae8; }
.btn-danger { background-color: #EA4335; border-color: #EA4335; } /* Google Red style */
.btn-danger:hover { background-color: #d13a2d; border-color: #d13a2d; }


@media (max-width: 768px) { .card-body { max-height: none; } .card { margin-bottom: 1rem; } }
</style>