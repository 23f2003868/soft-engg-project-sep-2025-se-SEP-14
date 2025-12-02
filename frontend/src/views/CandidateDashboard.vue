<template>
  <div class="candidate-dashboard-page">
    <!-- NAV -->
    <CandidateNavbar />

    <!-- SINGLE TOP-RIGHT TOAST CONTAINER -->
    <div class="toast-top-right" aria-live="polite" aria-atomic="true">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="neo-toast neo-toast-top"
        :class="'neo-toast-' + t.type"
        @mouseenter="pauseToast(t.id)"
        @mouseleave="resumeToast(t.id)"
      >
        <div class="neo-toast-inner">
          <div class="neo-toast-left"><i :class="t.icon"></i></div>
          <div class="neo-toast-body">
            <div class="neo-toast-title">{{ t.title }}</div>
            <div class="neo-toast-msg" v-html="t.message"></div>
            <div class="neo-toast-actions" v-if="t.action">
              <button class="btn btn-sm neo-toast-action" @click="runToastAction(t)">{{ t.action.label }}</button>
            </div>
          </div>
          <button class="neo-toast-close" @click="removeToast(t.id)">&times;</button>
        </div>
      </div>
    </div>

    <!-- MAIN -->
    <section class="candidate-dashboard-section py-4 py-md-5">
      <div class="container">
        <!-- HEADER -->
        <div class="row align-items-center mb-4 mb-md-5 fade-in visible">
          <div class="col-md-7">
            <p class="text-muted small mb-1">Candidate Dashboard</p>
            <h2 class="fw-bold text-primary mb-1">Welcome, {{ userProfile.name || "Candidate" }}</h2>
            <p class="text-secondary mb-0">Discover opportunities tailored to your skills and experience.</p>
          </div>

          <!-- STATS -->
          <div class="col-md-5 mt-3 mt-md-0">
            <div class="row g-2 g-md-3">
              <div class="col-4" v-for="card in statsCards" :key="card.key">
                <div class="stats-card d-flex align-items-center p-2 p-md-3 h-100">
                  <div class="stats-icon me-2"><i :class="'bi ' + card.icon"></i></div>
                  <div class="stats-text text-start">
                    <div class="stats-label small text-muted">{{ card.label }}</div>
                    <div class="stats-value fw-bold fs-6">{{ card.value }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FILTERS -->
        <div class="filter-card glass-card p-3 p-md-4 mb-4 fade-in visible">
          <div class="row g-3 align-items-center">
            <div class="col-lg-4">
              <label class="form-label small text-muted mb-1">Search</label>
              <div class="input-group search-box">
                <span class="input-group-text border-0 bg-transparent"><i class="bi bi-search text-primary"></i></span>
                <input v-model="searchQuery" type="text" class="form-control border-0" placeholder="Role, company, or location..." />
              </div>
            </div>

            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Job Type</label>
              <select v-model="jobTypeFilter" class="form-select form-select-sm rounded-3">
                <option value="">All</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Experience</label>
              <select v-model="experienceFilter" class="form-select form-select-sm rounded-3">
                <option value="">Any</option>
                <option value="0">Fresher (0 yrs)</option>
                <option value="1">1+ yrs</option>
                <option value="3">3+ yrs</option>
                <option value="5">5+ yrs</option>
                <option value="8">8+ yrs</option>
              </select>
            </div>

            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Location</label>
              <select v-model="locationFilter" class="form-select form-select-sm rounded-3">
                <option value="">Anywhere</option>
                <option v-for="loc in popularLocations" :key="loc" :value="loc">{{ loc }}</option>
              </select>
            </div>

            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Sort By</label>
              <select v-model="sortOption" class="form-select form-select-sm rounded-3">
                <option value="LATEST">Latest</option>
                <option value="EARLIEST">Oldest</option>
                <option value="EXP_ASC">Experience Low → High</option>
                <option value="EXP_DESC">Experience High → Low</option>
              </select>
            </div>
          </div>

          <div class="mt-3 d-flex flex-wrap align-items-center gap-2">
            <span class="small text-muted me-1">Filter by skills:</span>
            <button v-for="skill in allSkills" :key="skill" type="button" class="btn btn-sm skill-chip"
              :class="{ 'skill-chip-active': selectedSkills.includes(skill) }" @click="toggleSkill(skill)">{{ skill }}</button>

            <button v-if="selectedSkills.length" type="button" class="btn btn-sm btn-link text-decoration-none ms-1" @click="clearSkills">Clear</button>
          </div>
        </div>

        <!-- TABS -->
        <ul class="nav nav-pills mb-4 tab-pills fade-in visible">
          <li class="nav-item" v-for="tab in tabs" :key="tab.key">
            <button class="nav-link" :class="{ active: activeTab === tab.key }" @click="setTab(tab.key)">
              {{ tab.label }}
              <span v-if="tab.count !== undefined" class="badge rounded-pill ms-1 tab-count">{{ tab.count }}</span>
            </button>
          </li>
        </ul>

        <!-- JOB LIST -->
        <div v-if="loading" class="row g-4">
          <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
            <div class="job-card-skeleton glass-card p-4">
              <div class="skeleton-line w-50 mb-2"></div>
              <div class="skeleton-line w-25 mb-3"></div>
              <div class="skeleton-line w-75 mb-2"></div>
              <div class="skeleton-line w-50 mb-2"></div>
              <div class="skeleton-pill-group mt-3">
                <span class="skeleton-pill"></span><span class="skeleton-pill"></span><span class="skeleton-pill"></span>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <div v-if="visibleJobs.length" class="row g-4 fade-in visible">
            <div v-for="job in visibleJobs" :key="job.job_id" class="col-md-6 col-lg-4">
              <!-- INLINE Job Card -->
              <div class="job-card glass-card p-4 h-100 d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>
                    <div class="small text-muted"><i class="bi bi-geo-alt me-1 text-primary"></i>{{ job.location || "Location not specified" }}</div>
                  </div>

                  <span v-if="strongMatch(job)" class="badge rounded-pill bg-success-subtle text-success fw-semibold small-pill">Strong match</span>
                </div>

                <div class="small text-muted mb-1">
                  <span class="me-2"><i class="bi bi-briefcase me-1 text-primary"></i>{{ job.job_type }}</span>
                  <span><i class="bi bi-clock-history me-1 text-primary"></i>Posted {{ relativeDate(job.start_date) }}</span>
                </div>

                <div class="small text-muted mb-1">
                  <i class="bi bi-person-workspace me-1 text-primary"></i>
                  Experience: <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
                </div>

                <div class="small text-muted mb-2">
                  <i class="bi bi-calendar-event me-1 text-primary"></i>End Date: <span class="fw-semibold">{{ formatReadableDate(job.end_date) }}</span>
                </div>

                <p class="job-snippet text-secondary small flex-grow-1">{{ getShortDescription(job.description) }}</p>

                <div class="mb-3 d-flex flex-wrap gap-1">
                  <span v-for="skill in deriveJobSkills(job)" :key="skill" class="badge rounded-pill bg-light text-primary border small-pill">{{ skill }}</span>
                </div>

                <div class="d-flex justify-content-between align-items-center mt-2">
                  <button class="btn btn-sm btn-outline-primary rounded-pill" @click="openJobDetails(job)">
                    View Details
                  </button>

                  <div class="d-flex align-items-center gap-2">
                    <button class="btn btn-sm rounded-circle favorite-btn" :class="{ 'favorite-btn-active': isSaved(job) }" @click="toggleSave(job)">
                      <i :class="isSaved(job) ? 'bi bi-bookmark-fill' : 'bi bi-bookmark'"></i>
                    </button>

                    <button class="btn btn-sm btn-success rounded-pill"
                      :disabled="isApplied(job) || testHistory[job.job_id]"
                      @click="onApplyClick(job)">
                      {{ isApplied(job) ? "Applied" : (testHistory[job.job_id] ? "Test Done" : "Apply") }}
                    </button>
                  </div>
                </div>
              </div>
              <!-- END Job Card -->
            </div>
          </div>

          <div v-else class="text-center text-muted mt-5 fade-in visible">
            <i class="bi bi-briefcase fs-1 text-secondary d-block mb-3"></i>
            <p class="mb-1">No jobs match your current filters.</p>
            <p class="small">Try clearing some filters or switching the tab.</p>
            <button class="btn btn-outline-primary rounded-pill btn-sm mt-2" @click="resetFilters">Reset filters</button>
          </div>

          <div v-if="!loading && filteredJobs.length > jobsPerPage" class="d-flex justify-content-center mt-4">
            <button class="btn btn-outline-secondary rounded-pill btn-sm" v-if="visibleCount < filteredJobs.length" @click="loadMore">Load more jobs</button>
          </div>
        </div>
      </div>
    </section>

    <!-- JOB DETAILS MODAL (always in DOM so bootstrap can target it) -->
    <div class="modal fade" id="jobDetailsModal" tabindex="-1" aria-hidden="true" ref="jobDetailsModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header border-0">
            <div>
              <h5 class="modal-title fw-bold">{{ selectedJob?.job_title }}</h5>
              <p class="small text-muted mb-0">
                <i class="bi bi-geo-alt me-1 text-primary"></i>{{ selectedJob?.location }}
                •
                <i class="bi bi-briefcase ms-2 me-1 text-primary"></i>{{ selectedJob?.job_type }}
              </p>
              <p class="small text-muted mb-0">Experience: <span class="fw-semibold">{{ formatExperience(selectedJob?.experience) }}</span></p>
              <p class="small text-muted mb-0">End Date: <span class="fw-semibold">{{ formatReadableDate(selectedJob?.end_date) }}</span></p>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeJobDetails"></button>
          </div>

          <div class="modal-body pt-0">
            <hr class="mt-0 mb-3" />
            <h6 class="fw-semibold text-primary mb-2">Job Description</h6>
            <div class="small text-secondary mb-3 markdown-body" v-html="jobDescriptionHtml"></div>

            <h6 class="fw-semibold text-primary mb-2">Skills Highlight</h6>
            <div class="mb-3 d-flex flex-wrap gap-1">
              <span v-for="skill in deriveJobSkills(selectedJob || {})" :key="skill" class="badge rounded-pill bg-light text-primary border small-pill">{{ skill }}</span>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-2">
              <button class="btn btn-outline-primary btn-sm rounded-pill" @click="toggleSave(selectedJob)">
                <i :class="isSaved(selectedJob) ? 'bi bi-bookmark-fill me-1' : 'bi bi-bookmark me-1'"></i>{{ isSaved(selectedJob) ? "Saved" : "Save Job" }}
              </button>

              <button v-if="selectedJob" class="btn btn-success btn-sm rounded-pill" :disabled="isApplied(selectedJob) || testHistory[selectedJob.job_id]" @click="onApplyClick(selectedJob)">
                {{ isApplied(selectedJob) ? "Applied" : (testHistory[selectedJob.job_id] ? "Test Done" : "Apply") }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CREDIBILITY TEST MODAL (always in DOM) -->
    <div class="modal fade" id="credibilityTestModal" tabindex="-1" aria-hidden="true" ref="credibilityModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header border-0">
            <h5 class="modal-title fw-bold">Credibility Test</h5>
            <button type="button" class="btn-close" @click="cancelTest" :disabled="testSubmitting || testInProgress"></button>
          </div>

          <div class="modal-body">
            <div v-if="testJob">
              <p class="small text-muted mb-1">Job: <span class="fw-semibold">{{ testJob.job_title }}</span></p>
            </div>

            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <small class="text-muted">Question</small>
                <div class="fw-semibold">#{{ currentQIndex + 1 }} / {{ testQuestions.length }}</div>
              </div>
              <div class="text-end">
                <small class="text-muted">Time left</small>
                <div class="fw-semibold">{{ formatTimer(timeLeft) }}</div>
              </div>
            </div>

            <hr />

            <div v-if="testLoading" class="text-center py-4">
              <div class="spinner-border text-primary"></div>
              <div class="small text-muted mt-2">Loading test...</div>
            </div>

            <div v-else-if="testQuestions.length">
              <div class="mb-3">
                <p class="fw-semibold" v-html="sanitizeQuestion(currentQuestion.question)"></p>

                <div class="list-group">
                  <button v-for="(optText, optKey) in currentQuestion.options" :key="optKey" type="button"
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                    :class="{
                      active: answers[currentQIndex] === optKey,
                      'list-group-item-success': showCorrect && currentQuestion.correct_option === optKey,
                      'list-group-item-danger': showCorrect && answers[currentQIndex] === optKey && currentQuestion.correct_option !== optKey
                    }"
                    :disabled="showCorrect || !testInProgress"
                    @click="selectOption(optKey)">
                    <div class="text-start">
                      <span class="fw-semibold me-2">{{ optKey }}.</span>
                      <span v-html="sanitizeQuestion(optText)"></span>
                    </div>
                    <small v-if="showCorrect && currentQuestion.correct_option === optKey" class="text-success">Correct</small>
                  </button>
                </div>
              </div>

              <div class="d-flex justify-content-between mt-3">
                <div>
                  <button class="btn btn-sm btn-outline-secondary rounded-pill me-2" @click="prevQuestion" :disabled="currentQIndex === 0 || testLoading">Previous</button>
                  <button class="btn btn-sm btn-outline-secondary rounded-pill" @click="nextQuestion" :disabled="currentQIndex === testQuestions.length - 1 || testLoading">Next</button>
                </div>

                <div>
                  <button class="btn btn-sm btn-outline-danger rounded-pill me-2" @click="cancelTest" :disabled="testSubmitting || !testInProgress">Cancel</button>
                  <button class="btn btn-sm btn-success rounded-pill" @click="confirmSubmitTest" :disabled="testSubmitting || !testInProgress">Submit Test</button>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-4">
              <p class="small text-muted">No test available for this job.</p>
            </div>
          </div>

          <div class="modal-footer border-0">
            <small class="text-muted">Your answers are evaluated locally; only the final score is submitted.</small>
          </div>
        </div>
      </div>
    </div>

    <FloatingChatBot />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";

import CandidateNavbar from "../components/CandidateNavbar.vue";
import FloatingChatBot from "../components/ChatBot.vue";

/* -------------------------
   CONFIG & STATE
   ------------------------- */
const API_BASE = "http://127.0.0.1:5000/api";

const jobs = ref([]);
const loading = ref(false);
const selectedJob = ref(null);

const activeTab = ref("all");
const searchQuery = ref("");
const jobTypeFilter = ref("");
const experienceFilter = ref("");
const locationFilter = ref("");
const sortOption = ref("LATEST");
const selectedSkills = ref([]);

const visibleCount = ref(9);
const jobsPerPage = 9;

const resumeStatus = ref(null);
const resumeError = ref("");
const resumeSkills = ref([]);

const savedJobIds = ref(new Set());
const appliedJobIds = ref(new Set());
const testHistory = reactive({});

const popularLocations = ref(["Bangalore","Chennai","Hyderabad","Pune","Delhi NCR"]);
const allSkills = ref(["Python","SQL","VueJS","JavaScript","React","Node.js","Django","Flask","Machine Learning","Data Analysis"]);

const userProfile = ref({
  name: localStorage.getItem("firstname") || "Candidate",
  skills: ["Python","SQL","VueJS"],
});

/* -------------------------
   TOP-RIGHT TOASTS (SINGLE LIST)
   ------------------------- */
const toasts = ref([]);
let toastIdCounter = 1;
const toastTimers = new Map();

function nextToastId() { return `neo-${Date.now()}-${toastIdCounter++}`; }

function showToast({ type = "info", title = "", message = "", duration = 4200, action = null }) {
  const iconMap = { success: "bi bi-check-circle-fill", error: "bi bi-x-circle-fill", info: "bi bi-info-circle-fill" };
  const toast = { id: nextToastId(), type, title, message, icon: iconMap[type] || iconMap.info, duration, action, createdAt: Date.now() };
  toasts.value.unshift(toast);
  scheduleRemoval(toast.id, duration);
}

function scheduleRemoval(id, duration) {
  clearToastTimer(id);
  const timer = setTimeout(() => removeToast(id), duration);
  toastTimers.set(id, { timer, remaining: duration, start: Date.now() });
}

function pauseToast(id) {
  const entry = toastTimers.get(id);
  if (!entry) return;
  clearTimeout(entry.timer);
  const elapsed = Date.now() - entry.start;
  entry.remaining = Math.max(0, entry.remaining - elapsed);
  toastTimers.set(id, entry);
}

function resumeToast(id) {
  const entry = toastTimers.get(id);
  if (!entry) return;
  entry.start = Date.now();
  entry.timer = setTimeout(() => removeToast(id), entry.remaining);
  toastTimers.set(id, entry);
}

function clearToastTimer(id) { const e = toastTimers.get(id); if (!e) return; try { clearTimeout(e.timer); } catch {} toastTimers.delete(id); }

function removeToast(id) {
  const idx = toasts.value.findIndex(t => t.id === id);
  if (idx >= 0) toasts.value.splice(idx, 1);
  clearToastTimer(id);
}

function runToastAction(t) {
  if (!t || !t.action) return;
  try { t.action.handler(); } catch (e) { console.error("toast action failed", e); }
  removeToast(t.id);
}

/* Small helpers to create typed toasts */
function showSuccessToast(title, msg, opts = {}) { showToast({ type: "success", title, message: msg, duration: opts.duration || 4200, action: opts.action || null }); }
function showErrorToast(title, msg, opts = {}) { showToast({ type: "error", title, message: msg, duration: opts.duration ?? 0, action: opts.action || null }); }
function showInfoToast(title, msg, opts = {}) { showToast({ type: "info", title, message: msg, duration: opts.duration || 2000, action: opts.action || null }); }

/* -------------------------
   RESUME ONE-TIME NOTIFICATION LOGIC
   ------------------------- */
function getResumeNotified() {
  try {
    const raw = localStorage.getItem("resume_notified_status_v2");
    if (!raw) return null;
    return JSON.parse(raw);
  } catch (e) { return null; }
}
function setResumeNotified(status) {
  try { localStorage.setItem("resume_notified_status_v2", JSON.stringify({ status, at: Date.now() })); } catch(e){ }
}

/* When parsing fails, show a toast with Retry */
async function checkResumeStatusOnce() {
  try {
    const res = await fetch(`${API_BASE}/resume-status`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    const data = await res.json().catch(() => ({}));
    const status = (data.status || "").toUpperCase() || null;
    const error = data.error || "";

    resumeStatus.value = status;
    resumeError.value = error;
    resumeSkills.value = Array.isArray(data.skills) ? data.skills : (data.skills ? String(data.skills).split(",") : []);

    if (!status) return;

    const notified = getResumeNotified();
    if (notified && notified.status === status) return; // already shown same status

    if (status === "SUCCESS") {
      showSuccessToast("Resume parsed", "We parsed your resume successfully.");
      setResumeNotified("SUCCESS");
    } else if (status === "FAILED") {
      showErrorToast("Resume parsing failed", escapeHtml(error || "Resume parser failed"), {
        duration: 0,
        action: { label: "Retry", handler: () => doRetryParsing() }
      });
      setResumeNotified("FAILED");
    }
  } catch (err) {
    console.error("Error checking resume status:", err);
  }
}

async function doRetryParsing() {
  try {
    const res = await fetch(`${API_BASE}/resume-retry`, { method: "POST", headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      showErrorToast("Retry failed", escapeHtml(data.message || "Unable to restart parsing"));
      return;
    }
    showInfoToast("Retry started", escapeHtml(data.message || "Parsing restarted — we'll notify you when done."));
    // clear notified flag so next status is shown
    try { localStorage.removeItem("resume_notified_status_v2"); } catch {}
    setTimeout(checkResumeStatusOnce, 1500);
  } catch (err) {
    console.error("Retry parsing failed:", err);
    showErrorToast("Retry failed", "Unable to send retry request");
  }
}

/* -------------------------
   JOB / UI HELPERS (kept same logic)
   ------------------------- */
const statsCards = ref([
  { key: "total", label: "Total Jobs", value: 0, icon: "bi-briefcase-fill" },
  { key: "saved", label: "Saved Jobs", value: 0, icon: "bi-bookmark-heart-fill" },
  { key: "applied", label: "Applied", value: 0, icon: "bi-send-check-fill" },
]);

const recommendedJobs = computed(() => jobs.value.filter((job) => strongMatch(job)));
const tabs = computed(() => [
  { key: "all", label: "All Jobs" },
  { key: "recommended", label: "Recommended", count: recommendedJobs.value.length },
]);

const formatExperience = (exp) => {
  if (exp === null || exp === undefined || exp === "") return "Not specified";
  const n = Number(exp);
  if (Number.isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher (0 yrs)";
  if (n === 1) return "1 year";
  return `${n} years`;
};

const relativeDate = (dateStr) => {
  if (!dateStr) return "date unknown";
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return "date unknown";
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays <= 0) return "today";
  if (diffDays === 1) return "1 day ago";
  if (diffDays < 7) return `${diffDays} days ago`;
  const weeks = Math.floor(diffDays / 7);
  if (weeks < 4) return `${weeks} week${weeks > 1 ? "s" : ""} ago`;
  const months = Math.floor(diffDays / 30);
  return `${months || 1} month${months > 1 ? "s" : ""} ago`;
};

const formatReadableDate = (rawDate) => {
  if (!rawDate) return "Not specified";
  const d = new Date(rawDate);
  if (isNaN(d.getTime())) return "Not specified";
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
};

const getShortDescription = (desc) => {
  if (!desc) return "No description available.";
  let plain = String(desc);
  plain = plain.replace(/[#*_`>-]/g, " ").replace(/\[(.*?)\]\((.*?)\)/g, "$1").replace(/\s+/g, " ").trim();
  if (!plain.length) return "No description available.";
  if (plain.length <= 140) return plain;
  return plain.slice(0, 140) + "...";
};

const deriveJobSkills = (job) => {
  if (!job) return [];
  const text = (job.description || "").toLowerCase();
  const skillsSet = new Set();
  allSkills.value.forEach((skill) => { if (text.includes(skill.toLowerCase())) skillsSet.add(skill); });
  if (skillsSet.size === 0) return ["Communication", "Teamwork"];
  return Array.from(skillsSet).slice(0, 6);
};

const strongMatch = (job) => {
  if (!job) return false;
  const jobSkills = deriveJobSkills(job);
  if (!jobSkills.length) return false;
  const candidateSkills = userProfile.value.skills || [];
  if (!candidateSkills.length) return false;
  const intersection = jobSkills.filter((s) => candidateSkills.includes(s));
  return intersection.length >= 2;
};

const jobDescriptionHtml = computed(() => {
  if (!selectedJob.value || !selectedJob.value.description) return "<p>No detailed description available.</p>";
  return marked.parse(String(selectedJob.value.description));
});

/* -------------------------
   FILTERS & PAGINATION
   ------------------------- */
const filteredJobsBase = computed(() => {
  let list = [...jobs.value];
  if (activeTab.value === "recommended") list = list.filter((j) => strongMatch(j));
  else if (activeTab.value === "applied") list = list.filter((j) => appliedJobIds.value.has(j.job_id));
  else if (activeTab.value === "saved") list = list.filter((j) => savedJobIds.value.has(j.job_id));

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(job => {
      const title = (job.job_title || "").toLowerCase();
      const loc = (job.location || "").toLowerCase();
      const desc = (job.description || "").toLowerCase();
      return title.includes(q) || loc.includes(q) || desc.includes(q);
    });
  }

  if (jobTypeFilter.value) list = list.filter((job) => (job.job_type || "") === jobTypeFilter.value);

  if (experienceFilter.value !== "") {
    const minExp = Number(experienceFilter.value);
    list = list.filter((job) => Number(job.experience || 0) >= minExp);
  }

  if (locationFilter.value) {
    const loc = locationFilter.value.toLowerCase();
    list = list.filter((job) => (job.location || "").toLowerCase().includes(loc));
  }

  if (selectedSkills.value.length) {
    list = list.filter((job) => {
      const jobSkills = deriveJobSkills(job);
      return selectedSkills.value.every(sk => jobSkills.includes(sk));
    });
  }

  return list;
});

const filteredJobs = computed(() => {
  const list = [...filteredJobsBase.value];
  if (sortOption.value === "LATEST") return list.sort((a,b) => (b.start_date || "").localeCompare(a.start_date || ""));
  if (sortOption.value === "EARLIEST") return list.sort((a,b) => (a.start_date || "").localeCompare(b.start_date || ""));
  if (sortOption.value === "EXP_ASC") return list.sort((a,b) => Number(a.experience || 0) - Number(b.experience || 0));
  if (sortOption.value === "EXP_DESC") return list.sort((a,b) => Number(b.experience || 0) - Number(a.experience || 0));
  return list;
});

const visibleJobs = computed(() => filteredJobs.value.slice(0, visibleCount.value));
const loadMore = () => { visibleCount.value = Math.min(visibleCount.value + jobsPerPage, filteredJobs.value.length); };

const refreshStats = () => {
  const totalCard = statsCards.value.find(c => c.key === "total");
  const savedCard = statsCards.value.find(c => c.key === "saved");
  const appliedCard = statsCards.value.find(c => c.key === "applied");
  if (totalCard) totalCard.value = jobs.value.length;
  if (savedCard) savedCard.value = savedJobIds.value.size;
  if (appliedCard) appliedCard.value = appliedJobIds.value.size;
};

const isSaved = (job) => job && savedJobIds.value.has(job.job_id);
const isApplied = (job) => job && appliedJobIds.value.has(job.job_id);

/* -------------------------
   Save / Unsave
   ------------------------- */
const toggleSave = async (job) => {
  if (!job) return;
  const token = localStorage.getItem("token");
  if (!token) { showInfoToast("Not logged in","Please login again to save jobs."); return; }
  const alreadySaved = savedJobIds.value.has(job.job_id);
  try {
    if (alreadySaved) {
      const res = await fetch(`${API_BASE}/save-job/${job.job_id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` }});
      const data = await res.json().catch(()=>({}));
      if (!res.ok || data.success === false) { showErrorToast("Error", data.message || "Failed to remove from saved jobs."); return; }
      savedJobIds.value.delete(job.job_id); showInfoToast("Removed","Removed from saved jobs");
    } else {
      const res = await fetch(`${API_BASE}/save-job`, { method: "POST", headers: { "Content-Type":"application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ job_id: job.job_id })});
      const data = await res.json().catch(()=>({}));
      if (!res.ok || data.success === false) { showErrorToast("Error", data.message || "Failed to save job."); return; }
      savedJobIds.value.add(job.job_id); showSuccessToast("Saved","Job saved");
    }
    persistLocalState(); refreshStats();
  } catch (err) {
    showErrorToast("Error","Server error while updating saved jobs.");
  }
};

const persistLocalState = () => {
  try {
    const saveArr = Array.from(savedJobIds.value);
    const appliedArr = Array.from(appliedJobIds.value);
    localStorage.setItem("candidate_saved_jobs", JSON.stringify(saveArr));
    localStorage.setItem("candidate_applied_jobs", JSON.stringify(appliedArr));
  } catch (e) {}
};

const restoreLocalState = () => {
  try {
    const savedRaw = localStorage.getItem("candidate_saved_jobs");
    const appliedRaw = localStorage.getItem("candidate_applied_jobs");
    if (savedRaw) { const arr = JSON.parse(savedRaw); savedJobIds.value = new Set(arr); }
    if (appliedRaw) { const arr = JSON.parse(appliedRaw); appliedJobIds.value = new Set(arr); }
  } catch (e) {}
};

const fetchSavedJobs = async () => {
  const token = localStorage.getItem("token");
  if (!token) return;
  try {
    const res = await fetch(`${API_BASE}/saved-jobs-details`, { headers: { Authorization: `Bearer ${token}` }});
    const data = await res.json().catch(()=>({}));
    if (res.ok && data.success) {
      const ids = (data.jobs || []).map(j => j.job_id);
      savedJobIds.value = new Set(ids);
      persistLocalState(); refreshStats();
    }
  } catch (err) { console.error("Failed to fetch saved jobs", err); }
};

const loadJobs = async () => {
  loading.value = true;
  try {
    const res = await fetch(`${API_BASE}/jobs-all`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }});
    const data = await res.json().catch(()=>({}));
    if (!res.ok || data.success === false) { showErrorToast("Error", data.message || data.error || "Failed to load jobs for candidate."); jobs.value = []; }
    else { jobs.value = data.jobs || []; }
  } catch (err) {
    showErrorToast("Error","Server error while fetching jobs.");
    jobs.value = [];
  } finally {
    loading.value = false; refreshStats();
  }
};

/* -------------------------
   MOUNT / MODALS
   ------------------------- */
const jobDetailsModalRef = ref(null);
let jobDetailsModalInstance = null;

const credibilityModalRef = ref(null);
let credibilityModalInstance = null;

onMounted(() => {
  restoreLocalState();
  loadJobs();
  fetchSavedJobs();

  nextTick(() => { checkResumeStatusOnce(); });

  // initialize bootstrap modal instances AFTER DOM present
  nextTick(() => {
    if (jobDetailsModalRef.value) jobDetailsModalInstance = new Modal(jobDetailsModalRef.value);
    if (credibilityModalRef.value) credibilityModalInstance = new Modal(credibilityModalRef.value, { backdrop: "static", keyboard: false });
  });

  loadCredibilityHistory();
  window.addEventListener("saved-jobs-updated", () => { restoreLocalState(); refreshStats(); });
});

/* -------------------------
   Job Details open/close helpers
   ------------------------- */
const openJobDetails = (job) => {
  selectedJob.value = job;
  nextTick(() => { if (jobDetailsModalInstance) jobDetailsModalInstance.show(); });
};

const closeJobDetails = () => {
  selectedJob.value = null;
  if (jobDetailsModalInstance) jobDetailsModalInstance.hide();
};

/* -------------------------
   CREDIBILITY TEST (kept behaviour)
   ------------------------- */
const testJob = ref(null);
const testQuestions = ref([]);
const currentQIndex = ref(0);
const answers = ref({});
const timeLeft = ref(0);
const testTimeLimit = ref(0);
const testLoading = ref(false);
const testInProgress = ref(false);
const testSubmitting = ref(false);
const showCorrect = ref(false);
let testTimerInterval = null;
let applyAfterTestFlag = ref(false);

const formatTimer = (sec) => {
  if (sec == null || isNaN(sec)) return "00:00";
  const s = Math.max(0, Math.floor(sec));
  const mm = String(Math.floor(s/60)).padStart(2,"0");
  const ss = String(s%60).padStart(2,"0");
  return `${mm}:${ss}`;
};

const sanitizeQuestion = (q) => { if (!q) return ""; return String(q).replaceAll("<","&lt;").replaceAll(">","&gt;"); };
const currentQuestion = computed(()=> testQuestions.value[currentQIndex.value] || { question: "", options: {} });

function clearTestState(){
  testQuestions.value = []; currentQIndex.value = 0; answers.value = {}; timeLeft.value = 0; testTimeLimit.value = 0;
  testLoading.value = false; testInProgress.value = false; testSubmitting.value = false; showCorrect.value = false; applyAfterTestFlag.value = false;
  if (testTimerInterval) { clearInterval(testTimerInterval); testTimerInterval = null; }
}

const onApplyClick = async (job) => {
  if (appliedJobIds.value.has(job.job_id)) { showInfoToast("Already applied","You've already applied for this job."); return; }
  if (testHistory[job.job_id]) { showInfoToast("Test already completed","You have already completed the credibility test for this job."); return; }
  startCredibilityTest(job, { autoApplyAfter: true });
};

async function startCredibilityTest(job, opts = {}) {
  testJob.value = job;
  applyAfterTestFlag.value = !!opts.autoApplyAfter;
  clearTestState();
  testLoading.value = true;

  nextTick(() => { if (credibilityModalInstance) credibilityModalInstance.show(); });

  try {
    const token = localStorage.getItem("token");
    if (!token) { testLoading.value = false; showErrorToast("Not logged in","Please login to take the test."); return; }

    const res = await fetch(`${API_BASE}/credibility-test/${job.job_id}`, { headers: { Authorization: `Bearer ${token}` }});
    const text = await res.text();
    let data = null;
    try { data = JSON.parse(text); } catch(e){ data = null; }

    if (!res.ok || !data || !Array.isArray(data.questions)) {
      testLoading.value = false;
      const msg = data && data.message ? data.message : "Unable to fetch test. Try again later.";
      showErrorToast("Test unavailable", msg);
      return;
    }

    testQuestions.value = data.questions.map((q) => {
      const optsObj = q.options || {};
      return { question: q.question || "", options: { A: optsObj.A || "", B: optsObj.B || "", C: optsObj.C || "", D: optsObj.D || "" }, correct_option: (q.correct_option || "").toUpperCase() };
    });

    const tlimit = Number(data.time_limit || data.timeLimit || data.time || 0);
    testTimeLimit.value = (tlimit && !isNaN(tlimit)) ? tlimit : (testQuestions.value.length ? 120 : 60);
    timeLeft.value = testTimeLimit.value;

    testLoading.value = false; testInProgress.value = true; startTestTimer();
    showInfoToast("Test started", `You have ${formatTimer(timeLeft.value)} to complete the test.`);
  } catch (err) {
    testLoading.value = false; console.error("Failed to fetch test:", err); showErrorToast("Error","Server error while fetching test.");
  }
}

function startTestTimer() {
  if (testTimerInterval) clearInterval(testTimerInterval);
  testTimerInterval = setInterval(()=> {
    timeLeft.value = Math.max(0, timeLeft.value - 1);
    if (timeLeft.value <= 0) { clearInterval(testTimerInterval); testTimerInterval = null; autoSubmitOnTimeout(); }
  }, 1000);
}

function autoSubmitOnTimeout() {
  if (testInProgress.value && !testSubmitting.value) { showInfoToast("Time's up","Submitting your answers..."); submitTest(); }
}

function selectOption(optKey) { if (!testInProgress.value || showCorrect.value) return; answers.value = { ...answers.value, [currentQIndex.value]: optKey }; }
function prevQuestion(){ if (currentQIndex.value > 0) currentQIndex.value -= 1; }
function nextQuestion(){ if (currentQIndex.value < testQuestions.value.length - 1) currentQIndex.value += 1; }

async function confirmSubmitTest() {
  if (!testInProgress.value || testSubmitting.value) return;
  const result = await Swal.fire({
    title: "Submit test?",
    text: "Your answers will be evaluated locally and only final score will be submitted.",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Submit",
    cancelButtonText: "Continue test",
    reverseButtons: true,
  });
  if (result.isConfirmed) submitTest();
}

async function submitTest() {
  if (!testInProgress.value || testSubmitting.value) return;
  testSubmitting.value = true;
  try {
    if (testTimerInterval) { clearInterval(testTimerInterval); testTimerInterval = null; }

    let correctCount = 0;
    for (let i = 0; i < testQuestions.value.length; i++) {
      const q = testQuestions.value[i];
      const ans = (answers.value[i] || "").toUpperCase();
      if (ans && q.correct_option && ans === q.correct_option) correctCount += 1;
    }

    const scorePercent = Math.round((correctCount / Math.max(1, testQuestions.value.length)) * 100);
    showCorrect.value = true;
    testInProgress.value = false;

    // block re-take locally
    testHistory[testJob.value.job_id] = true;

    const token = localStorage.getItem("token");
    if (!token) { testSubmitting.value = false; showErrorToast("Not logged in","Please login to submit the test."); return; }

    const res = await fetch(`${API_BASE}/credibility-test/${testJob.value.job_id}`, {
      method: "POST",
      headers: { "Content-Type":"application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ score: scorePercent }),
    });
    const data = await res.json().catch(()=>({}));
    if (!res.ok) {
      showErrorToast("Submit failed", data.error || data.message || "Unable to submit score.");
      if (!data.message || !String(data.message).toLowerCase().includes("already")) delete testHistory[testJob.value.job_id];
      testSubmitting.value = false; return;
    }

    showSuccessToast("Test completed", `Score: ${scorePercent}%`);

    if (data.status && data.status === "APPLIED") {
      appliedJobIds.value.add(testJob.value.job_id);
    } else {
      await attemptApplyAfterTest(testJob.value);
    }

    persistLocalState(); refreshStats();
    testSubmitting.value = false;

    setTimeout(()=> {
      if (credibilityModalInstance) credibilityModalInstance.hide();
      setTimeout(clearTestState, 700);
    }, 900);
  } catch(err) {
    console.error("submitTest error", err);
    testSubmitting.value = false;
    delete testHistory[testJob.value.job_id];
    showErrorToast("Submit error", "Network error while submitting score.");
  }
}

async function attemptApplyAfterTest(job) {
  if (!job) return;
  const token = localStorage.getItem("token");
  if (!token) { showErrorToast("Not logged in","Please login to apply."); return; }
  try {
    const res = await fetch(`${API_BASE}/job-apply`, {
      method: "POST",
      headers: { "Content-Type":"application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ job_id: job.job_id }),
    });
    const data = await res.json().catch(()=>({}));
    if (!res.ok) {
      showInfoToast("Apply", data.message || data.error || "Unable to apply automatically. Please try applying from job details.");
      return;
    }
    if (data.success || res.status === 200) {
      appliedJobIds.value.add(job.job_id);
      testHistory[job.job_id] = true;
      persistLocalState(); refreshStats();
      showSuccessToast("Applied", "Your application was submitted.");
    } else {
      showInfoToast("Apply", data.message || "Apply completed with warnings.");
    }
  } catch (err) {
    console.error("apply error", err); showErrorToast("Apply failed","Network error while applying.");
  }
}

function cancelTest() {
  if (testInProgress.value && !testSubmitting.value) {
    Swal.fire({
      title: "Cancel test?",
      text: "Your progress will be lost. Are you sure?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, cancel",
      cancelButtonText: "Continue",
    }).then((r) => {
      if (r.isConfirmed) {
        if (testTimerInterval) { clearInterval(testTimerInterval); testTimerInterval = null; }
        clearTestState();
        if (credibilityModalInstance) credibilityModalInstance.hide();
        showInfoToast("Test cancelled", "You can retry later.");
      }
    });
  } else {
    clearTestState();
    if (credibilityModalInstance) credibilityModalInstance.hide();
  }
}

/* -------------------------
   load credibility history
   ------------------------- */
async function loadCredibilityHistory() {
  try {
    const token = localStorage.getItem("token");
    if (!token) return;
    const res = await fetch(`${API_BASE}/credibility-history`, { headers: { Authorization: `Bearer ${token}` }});
    const data = await res.json().catch(()=>({}));
    if (res.ok && data.success) {
      const map = {};
      (data.history || []).forEach(h => { if (h.job_id) map[h.job_id] = true; });
      Object.keys(testHistory).forEach(k => delete testHistory[k]);
      Object.assign(testHistory, map);
    }
  } catch (err) { console.error("loadCredibilityHistory error", err); }
}

/* -------------------------
   UI helpers
   ------------------------- */
const toggleSkill = (skill) => { const idx = selectedSkills.value.indexOf(skill); if (idx >= 0) selectedSkills.value.splice(idx,1); else selectedSkills.value.push(skill); };
const clearSkills = () => { selectedSkills.value = []; };
const setTab = (tabKey) => { activeTab.value = tabKey; visibleCount.value = jobsPerPage; };
const resetFilters = () => {
  searchQuery.value = ""; jobTypeFilter.value = ""; experienceFilter.value = ""; locationFilter.value = ""; sortOption.value = "LATEST";
  selectedSkills.value = []; activeTab.value = "all"; visibleCount.value = jobsPerPage;
};

/* -------------------------
   small utility
   ------------------------- */
function escapeHtml(unsafe) {
  if (!unsafe) return "";
  return String(unsafe).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'", "&#039;");
}

/* expose certain utilities implicitly (script-setup unwrapped works in template) */

</script>

<style scoped>
/* --- Toast (top-right) --- */
.toast-top-right {
  position: fixed;
  top: 18px;
  right: 18px;
  z-index: 1080;
  display:flex;
  flex-direction:column;
  gap:10px;
  pointer-events:none;
  max-width: 380px;
  width: auto;
}

.neo-toast {
  pointer-events: auto;
  width: 100%;
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.94);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.6);
  padding: 10px 12px;
  display:flex;
  box-shadow: 0 12px 28px rgba(2,6,23,0.14);
  transform: translateY(-6px);
  animation: toastIn 0.28s ease forwards;
}

.neo-toast-top { }
.neo-toast-success { border-left: 4px solid #28a745; }
.neo-toast-error { border-left: 4px solid #dc3545; }
.neo-toast-info { border-left: 4px solid #0d6efd; }

.neo-toast-inner { display:flex; gap:10px; width:100%; align-items:flex-start; }
.neo-toast-left { font-size:1.2rem; color:#0b3b5b; margin-top:2px; }
.neo-toast-body { flex:1; }
.neo-toast-title { font-weight:600; font-size:0.94rem; color:#042a46; margin-bottom:2px; }
.neo-toast-msg { font-size:0.86rem; color:#234a66; line-height:1.22; }
.neo-toast-actions { margin-top:6px; }
.neo-toast-action { background: rgba(0,114,255,0.08); border:1px solid rgba(0,114,255,0.1); color:#0a3d62; padding:6px 10px; border-radius:8px; font-size:0.82rem; }
.neo-toast-close { background: transparent; border: none; font-size:18px; color:#234a66; margin-left:8px; opacity:0.7; cursor:pointer; }

/* animation */
@keyframes toastIn { from { opacity:0; transform: translateY(-8px) scale(0.98); } to { opacity:1; transform: translateY(0) scale(1); } }

/* Page background */
.candidate-dashboard-page { min-height:100vh; background: radial-gradient(circle at top left, #e0edff, #eef4ff 40%, #e7f1ff 70%, #dde8ff); }
.candidate-dashboard-section { min-height: calc(100vh - 70px); }

.fade-in.visible { animation: fadeInUp 0.6s ease forwards; }
@keyframes fadeInUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }

.glass-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(14px); border-radius:1.5rem; border:1px solid rgba(255,255,255,0.8); box-shadow:0 14px 30px rgba(15,23,42,0.12); }

/* stats */
.stats-card { border-radius:1.1rem; background: linear-gradient(135deg,#ffffff,#edf2ff); box-shadow:0 10px 22px rgba(15,23,42,0.12); border:1px solid rgba(148,163,184,0.2); min-height:110px; display:flex; }
.stats-icon { width:38px; height:38px; border-radius:999px; display:flex; align-items:center; justify-content:center; background: radial-gradient(circle at 20% 20%, #0d6efd, #2563eb); color:#fff; font-size:1.1rem; }

/* skill chips */
.skill-chip { border-radius:999px; border:1px solid rgba(148,163,184,0.4); background: rgba(255,255,255,0.9); font-size:0.8rem; padding:4px 12px; }
.skill-chip-active { background: linear-gradient(90deg,#0072ff,#00c6ff); color:#fff; border-color:transparent; }

/* tabs */
.tab-pills .nav-link { border-radius:999px; font-size:0.85rem; padding-inline:16px; padding-block:6px; color:#0d6efd; }
.tab-pills .nav-link.active { background:#0d6efd; color:#fff; }

/* job card */
.job-card { border-radius:1.4rem; transition: transform 0.25s ease, box-shadow 0.25s ease; }
.job-card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(15,23,42,0.22); }
.job-snippet { line-height:1.4; }
.favorite-btn { width:32px; height:32px; border-radius:999px; border:1px solid rgba(148,163,184,0.55); display:inline-flex; align-items:center; justify-content:center; background: rgba(255,255,255,0.95); font-size:1.1rem; transition:0.2s ease; }
.favorite-btn-active { border-color:transparent; background:#e0f2fe; color:#0ea5e9; }

/* skeleton */
.job-card-skeleton { border-radius:1.4rem; position:relative; overflow:hidden; }
.skeleton-line { height:10px; border-radius:999px; background: linear-gradient(90deg,#edf2ff 0%, #e2e8f0 50%, #edf2ff 100%); animation: shimmer 1.3s infinite linear; margin-bottom:8px; }
.skeleton-pill-group { display:flex; gap:6px; }
.skeleton-pill { width:60px; height:18px; border-radius:999px; background: linear-gradient(90deg,#edf2ff 0%, #e2e8f0 50%, #edf2ff 100%); animation: shimmer 1.3s infinite linear; }
@keyframes shimmer { 0% { transform: translateX(-10%); } 100% { transform: translateX(10%); } }

/* modal glass */
.glass-modal { background: rgba(255,255,255,0.96); backdrop-filter: blur(18px); border-radius:1.4rem; }
.markdown-body { line-height:1.5; }
.small-pill { font-size:0.75rem; padding-inline:10px; padding-block:4px; }

/* answers highlight */
.list-group-item-success { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.18); }
.list-group-item-danger { background: rgba(220,53,69,0.06); border-color: rgba(220,53,69,0.12); }
</style>
