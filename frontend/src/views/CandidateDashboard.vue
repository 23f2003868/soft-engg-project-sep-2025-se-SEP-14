<template>
  <div class="candidate-dashboard-page">

    <!-- NAV -->
    <CandidateNavbar />

    <!-- TOASTS -->
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

            <div v-if="t.action" class="neo-toast-actions">
              <button class="btn btn-sm neo-toast-action" @click="runToastAction(t)">
                {{ t.action.label }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MAIN SECTION -->
    <section class="candidate-dashboard-section py-4 py-md-5">
      <div class="container">

        <!-- HEADER + STATS -->
        <div class="row align-items-center mb-4 mb-md-5 fade-in visible">
          <div class="col-md-7">
            <p class="text-muted small mb-1">Candidate Dashboard</p>
            <h2 class="fw-bold text-primary mb-1">Welcome, {{ userProfile.name }}</h2>
            <p class="text-secondary">Discover opportunities tailored for you.</p>
          </div>

          <div class="col-md-5 mt-3 mt-md-0">
            <div class="row g-3">
              <div class="col-4" v-for="card in statsCards" :key="card.key">
                <div class="stats-card d-flex align-items-center p-3 h-100">
                  <div class="stats-icon me-2">
                    <i :class="'bi ' + card.icon"></i>
                  </div>
                  <div>
                    <div class="small text-muted">{{ card.label }}</div>
                    <div class="fw-bold fs-6">{{ card.value }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FILTER BAR -->
        <div class="filter-card glass-card p-3 p-md-4 mb-4 fade-in visible">
          <div class="row g-3 align-items-center">

            <div class="col-lg-4">
              <label class="form-label small text-muted mb-1">Search</label>
              <div class="input-group search-box">
                <span class="input-group-text bg-transparent border-0">
                  <i class="bi bi-search text-primary"></i>
                </span>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control border-0"
                  placeholder="Role, company, or location..."
                />
              </div>
            </div>

            <!-- Job type -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Job Type</label>
              <select v-model="jobTypeFilter" class="form-select form-select-sm rounded-3">
                <option value="">All</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <!-- Experience -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Experience</label>
              <select v-model="experienceFilter" class="form-select form-select-sm rounded-3">
                <option value="">Any</option>
                <option value="0">Fresher</option>
                <option value="1">1+ yrs</option>
                <option value="3">3+ yrs</option>
                <option value="5">5+ yrs</option>
                <option value="8">8+ yrs</option>
              </select>
            </div>

            <!-- Location filter -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Location</label>
              <select v-model="locationFilter" class="form-select form-select-sm rounded-3">
                <option value="">Anywhere</option>
                <option v-for="loc in popularLocations" :key="loc">{{ loc }}</option>
              </select>
            </div>

            <!-- Sort -->
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

          <!-- Skills chips -->
          <div class="mt-3 d-flex flex-wrap gap-2">
            <span class="small text-muted">Filter by skills:</span>

            <button
              v-for="skill in allSkills"
              :key="skill"
              class="btn btn-sm skill-chip"
              :class="{ 'skill-chip-active': selectedSkills.includes(skill) }"
              @click="toggleSkill(skill)"
            >
              {{ skill }}
            </button>

            <button
              v-if="selectedSkills.length"
              class="btn btn-sm btn-link text-decoration-none"
              @click="clearSkills"
            >
              Clear
            </button>
          </div>
        </div>

        <!-- TABS -->
        <ul class="nav nav-pills mb-4 tab-pills fade-in visible">
          <li class="nav-item" v-for="tab in tabs" :key="tab.key">
            <button
              class="nav-link"
              :class="{ active: activeTab === tab.key }"
              @click="setTab(tab.key)"
            >
              {{ tab.label }}
              <span v-if="tab.count" class="badge rounded-pill ms-1 tab-count">{{ tab.count }}</span>
            </button>
          </li>
        </ul>

        <!-- SKELETON LOADER -->
        <div v-if="loading" class="row g-4">
          <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
            <div class="job-card-skeleton glass-card p-4"></div>
          </div>
        </div>

        <!-- JOB CARDS -->
        <div v-else>
          <div v-if="visibleJobs.length" class="row g-4 fade-in visible">

            <div
              v-for="job in visibleJobs"
              :key="job.job_id"
              class="col-md-6 col-lg-4"
            >
              <div class="job-card glass-card p-4 d-flex flex-column h-100">

                <!-- Title + Company + Location -->
                <div class="d-flex justify-content-between align-items-start mb-3">

                  <!-- Avatar -->
                  <div class="job-avatar">
                    <img :src="generateJobAvatar(job.job_title)" />
                  </div>

                  <div class="flex-grow-1 ms-3">

                    <!-- Job Title -->
                    <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>

                    <!-- Company Name (NEW) -->
                    <div class="small text-primary fw-semibold mb-1">
                      <i class="bi bi-building me-1"></i>
                      {{ job.company || "Unknown Company" }}
                    </div>

                    <!-- Location -->
                    <div class="small text-muted">
                      <i class="bi bi-geo-alt me-1 text-primary"></i>{{ job.location }}
                    </div>
                  </div>

                  <span
                    v-if="strongMatch(job)"
                    class="badge rounded-pill bg-success-subtle text-success fw-semibold small-pill"
                  >
                    Strong match
                  </span>
                </div>

                <!-- Job Meta -->
                <div class="small text-muted mb-1">
                  <i class="bi bi-briefcase me-1 text-primary"></i>{{ job.job_type }}
                  •
                  <i class="bi bi-clock-history ms-1 me-1 text-primary"></i>{{ relativeDate(job.start_date) }}
                </div>

                <div class="small text-muted mb-1">
                  <i class="bi bi-person-workspace me-1 text-primary"></i>
                  Experience: <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
                </div>

                <div class="small text-muted mb-2">
                  <i class="bi bi-calendar-event me-1 text-primary"></i>
                  End Date: {{ formatReadableDate(job.end_date) }}
                </div>

                <!-- Description -->
                <p class="job-snippet text-secondary small mt-2 mb-3">
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

                <!-- Bottom Buttons -->
                <div class="d-flex justify-content-between align-items-center mt-auto">

                  <button
                    class="btn btn-sm btn-outline-primary rounded-pill"
                    @click="openJobDetails(job)"
                  >
                    View Details
                  </button>
                  <button
                    class="btn btn-sm chat-btn rounded-circle"
                    @click="openChatForJob(job)"
                  >
                    <i class="bi bi-robot"></i>
                  </button>
                  <div class="d-flex gap-2">
                    <button
                      class="btn btn-sm rounded-circle favorite-btn"
                      :class="{ 'favorite-btn-active': isSaved(job) }"
                      @click="toggleSave(job)"
                    >
                      <i :class="isSaved(job) ? 'bi bi-bookmark-fill' : 'bi bi-bookmark'"></i>
                    </button>

                    <button
                      class="btn btn-sm btn-success rounded-pill"
                      :disabled="isApplied(job) || testHistory[job.job_id]"
                      @click="onApplyClick(job)"
                    >
                      {{ isApplied(job) ? "Applied"
                        : testHistory[job.job_id] ? "Test Done"
                        : "Apply" }}
                    </button>
                  </div>
                </div>
              </div>

            </div>

          </div>

          <!-- No jobs -->
          <div v-else class="text-center text-muted mt-5 fade-in">
            <i class="bi bi-briefcase fs-1 text-secondary mb-3"></i>
            <p>No jobs match your filters.</p>
            <button class="btn btn-outline-primary rounded-pill btn-sm" @click="resetFilters">
              Reset filters
            </button>
          </div>

          <!-- LOAD MORE -->
          <div v-if="visibleJobs.length < filteredJobs.length" class="d-flex justify-content-center mt-4">
            <button class="btn btn-outline-secondary rounded-pill btn-sm" @click="loadMore">
              Load more jobs
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- JOB DETAILS MODAL -->
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
              </p>

              <p class="small text-muted">
                End Date: {{ formatReadableDate(selectedJob.end_date) }}
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
                class="btn btn-outline-primary btn-sm rounded-pill"
                @click="toggleSave(selectedJob)"
              >
                <i :class="isSaved(selectedJob) ? 'bi bi-bookmark-fill me-1' : 'bi bi-bookmark me-1'"></i>
                {{ isSaved(selectedJob) ? "Saved" : "Save Job" }}
              </button>

              <button
                class="btn btn-success btn-sm rounded-pill"
                :disabled="isApplied(selectedJob) || testHistory[selectedJob.job_id]"
                @click="onApplyClick(selectedJob)"
              >
                {{ isApplied(selectedJob) ? "Applied"
                  : testHistory[selectedJob.job_id] ? "Test Done"
                  : "Apply" }}
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- TEST MODAL -->
    <div class="modal fade" id="credibilityTestModal" tabindex="-1" ref="credibilityModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">

          <div class="modal-header border-0">
            <h5 class="modal-title fw-bold">Credibility Test</h5>
          </div>

          <div class="modal-body">
            <div v-if="testJob">
              <p class="small text-muted">Job: <strong>{{ testJob.job_title }}</strong></p>
            </div>

            <div class="d-flex justify-content-between mb-2">
              <div>
                <small class="text-muted">Question</small>
                <div class="fw-semibold">
                  {{ currentQIndex + 1 }} / {{ testQuestions.length }}
                </div>
              </div>
              <div>
                <small class="text-muted">Time left</small>
                <div class="fw-semibold">{{ formatTimer(timeLeft) }}</div>
              </div>
            </div>

            <hr />

            <!-- If loading -->
            <div v-if="testLoading" class="text-center py-4">
              <div class="spinner-border text-primary"></div>
            </div>

            <!-- Questions -->
            <div v-else-if="testQuestions.length">

              <p class="fw-semibold" v-html="sanitizeQuestion(currentQuestion.question)"></p>

              <div class="list-group">
                <button
                  v-for="(opt, key) in currentQuestion.options"
                  :key="key"
                  type="button"
                  class="list-group-item list-group-item-action"
                  :class="{
                    active: answers[currentQIndex] === key,
                    'list-group-item-success': showCorrect && currentQuestion.correct_option === key,
                    'list-group-item-danger': showCorrect && answers[currentQIndex] === key &&
                                                currentQuestion.correct_option !== key
                  }"
                  :disabled="showCorrect"
                  @click="selectOption(key)"
                >
                  <strong>{{ key }}.</strong> <span v-html="sanitizeQuestion(opt)"></span>
                </button>
              </div>

              <!-- Navigation -->
              <div class="d-flex justify-content-between mt-3">
                <button
                  class="btn btn-sm btn-outline-secondary rounded-pill"
                  :disabled="currentQIndex === 0"
                  @click="prevQuestion"
                >
                  Previous
                </button>

                <button
                  class="btn btn-sm btn-outline-secondary rounded-pill"
                  :disabled="currentQIndex >= testQuestions.length - 1"
                  @click="nextQuestion"
                >
                  Next
                </button>

                <button
                  class="btn btn-sm btn-success rounded-pill"
                  @click="confirmSubmitTest"
                >
                  Submit Test
                </button>
              </div>
            </div>

            <div v-else class="text-center py-4">
              No test available.
            </div>
          </div>

        </div>
      </div>
    </div>

<!-- CHATBOT MODAL -->
<div class="modal fade" id="jobChatbotModal" tabindex="-1" ref="chatbotModalRef" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content border-0">          <!-- <- IMPORTANT: modal-content wrapper -->
      <div class="chatbot-wrapper">

        <!-- HEADER -->
        <div class="chatbot-header d-flex align-items-center">
          <div class="bot-avatar">
            <i class="bi bi-robot"></i>
          </div>

          <div class="ms-3">
            <h5 class="mb-0 fw-bold">{{ chatbotJob?.job_title }}</h5>
            <p class="small text-muted mb-0">{{ chatbotJob?.company }}</p>
          </div>
          <button
            class="btn btn-sm btn-outline-primary rounded-pill me-2"
            @click="clearChatConversation"
          >
            <i class="bi bi-trash"></i> Clear Chat
          </button>
          <button class="btn-close ms-auto" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <!-- CHAT BODY -->
        <div class="chatbot-body" ref="chatBodyRef" role="log" aria-live="polite">
          <div
            v-for="msg in chatMessages"
            :key="msg.id"
            :class="msg.sender === 'user' ? 'msg msg-user' : 'msg msg-ai'"
          >
            <div v-if="msg.sender==='ai'" class="bubble" v-html="marked.parse(msg.text)"></div>
            <div v-else class="bubble" >{{ msg.text }}</div>
          </div>

          <!-- Typing indicator -->
          <div v-if="botTyping" class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>

        <!-- INPUT BAR -->
        <div class="chatbot-input">
          <input
            ref="chatInputRef"
            v-model="chatInput"
            @keyup.enter="sendChatMsg"
            aria-label="Chat message"
            placeholder="Ask something about this job..."
            autocomplete="off"
          />
          <button @click="sendChatMsg" aria-label="Send message">
            <i class="bi bi-send-fill"></i>
          </button>
        </div>

      </div>
    </div>
  </div>
</div>

  </div>
</template>

<script setup>
/* -------------------------------------------------------
   Imports
------------------------------------------------------- */
import { ref, reactive, computed, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";

import CandidateNavbar from "../components/CandidateNavbar.vue";

/* -------------------------------------------------------
   Constants / Base State
------------------------------------------------------- */
const API_BASE = "http://127.0.0.1:5000/api";

const jobs = ref([]);
const loading = ref(false);

const selectedJob = ref({ job_title: "", location: "", job_type: "", experience: "", end_date: "", description: "" });

const activeTab = ref("all");

const searchQuery = ref("");
const jobTypeFilter = ref("");
const experienceFilter = ref("");
const locationFilter = ref("");
const sortOption = ref("LATEST");
const selectedSkills = ref([]);

const visibleCount = ref(9);
const jobsPerPage = 9;

const savedJobIds = ref(new Set());
const appliedJobIds = ref(new Set());
const testHistory = reactive({});

const resumeStatus = ref(null);
const resumeError = ref("");
const resumeSkills = ref([]);

const chatbotModalRef = ref(null);
let chatbotModalInstance = null;

const chatbotJob = ref(null);
const chatMessages = ref([]);
const chatInput = ref("");
const botTyping = ref(false);
const chatBodyRef = ref(null);

const popularLocations = ref(["Bangalore", "Chennai", "Hyderabad", "Pune", "Delhi NCR"]);

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

const userProfile = ref({
  name: localStorage.getItem("firstname") || "Candidate",
  skills: ["Python", "SQL", "VueJS"]
});

/* -------------------------------------------------------
   Toast System (Top-Right)
------------------------------------------------------- */
const toasts = ref([]);
let toastCounter = 1;
const toastTimers = new Map();

function nextToastId() {
  return `toast-${Date.now()}-${toastCounter++}`;
}

function showToast({ type = "info", title = "", message = "", duration = 4000, action = null }) {
  const icons = {
    success: "bi bi-check-circle-fill",
    error: "bi bi-x-circle-fill",
    info: "bi bi-info-circle-fill"
  };

  const toast = {
    id: nextToastId(),
    type,
    title,
    message,
    icon: icons[type],
    duration,
    action,
    createdAt: Date.now()
  };

  toasts.value.unshift(toast);
  scheduleRemoval(toast.id, duration);
}

function scheduleRemoval(id, duration) {
  clearTimer(id);
  const timer = setTimeout(() => removeToast(id), duration);
  toastTimers.set(id, { timer, remaining: duration, start: Date.now() });
}

function pauseToast(id) {
  const t = toastTimers.get(id);
  if (!t) return;
  clearTimeout(t.timer);
  const elapsed = Date.now() - t.start;
  t.remaining = Math.max(0, t.remaining - elapsed);
}

function resumeToast(id) {
  const t = toastTimers.get(id);
  if (!t) return;
  t.start = Date.now();
  t.timer = setTimeout(() => removeToast(id), t.remaining);
}

function clearTimer(id) {
  const t = toastTimers.get(id);
  if (!t) return;
  clearTimeout(t.timer);
  toastTimers.delete(id);
}

function removeToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id);
  clearTimer(id);
}

function runToastAction(t) {
  if (t.action && t.action.handler) t.action.handler();
  removeToast(t.id);
}

const showSuccessToast = (title, msg) => showToast({ type: "success", title, message: msg });
const showErrorToast = (title, msg) => showToast({ type: "error", title, message: msg, duration: 0 });
const showInfoToast = (title, msg) => showToast({ type: "info", title, message: msg });

/* -------------------------------------------------------
   Persistence keys (per-user)
   We'll namespace localStorage keys to avoid cross-user collisions.
------------------------------------------------------- */
function getUserKeyPrefix() {
  // prefer stable unique value if your app stores it (email, user_id). fallbacks to firstname.
  const email = localStorage.getItem("email") || localStorage.getItem("user_email");
  const uid = email || localStorage.getItem("firstname") || "anon";
  return `candidate_${uid}_`;
}

/* -------------------------------------------------------
   Resume Parsing One-Time Notification
------------------------------------------------------- */
function getResumeNotified() {
  try {
    return JSON.parse(localStorage.getItem("resume_notified_v2"));
  } catch {
    return null;
  }
}

function setResumeNotified(status) {
  localStorage.setItem("resume_notified_v2", JSON.stringify({ status, at: Date.now() }));
}

async function checkResumeStatusOnce() {
  try {
    const res = await fetch(`${API_BASE}/resume-status`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });

    const data = await res.json();

    resumeStatus.value = data.status || "";
    resumeError.value = data.error || "";
    resumeSkills.value = Array.isArray(data.skills) ? data.skills : [];

    const notified = getResumeNotified();
    if (notified && notified.status === resumeStatus.value) return;

    if (resumeStatus.value === "SUCCESS") {
      showSuccessToast("Resume parsed", "Your resume was processed successfully.");
      setResumeNotified("SUCCESS");
    } else if (resumeStatus.value === "FAILED") {
      showErrorToast("Parsing failed", resumeError.value || "Resume parsing failed.");
      setResumeNotified("FAILED");
    }
  } catch {}
}

/* -------------------------------------------------------
   Stats Cards
------------------------------------------------------- */
const statsCards = ref([
  { key: "total", label: "Total Jobs", value: 0, icon: "bi-briefcase-fill" },
  { key: "saved", label: "Saved Jobs", value: 0, icon: "bi-bookmark-heart-fill" },
  { key: "applied", label: "Applied", value: 0, icon: "bi-send-check-fill" }
]);

function refreshStats() {
  statsCards.value.find(c => c.key === "total").value = jobs.value.length;
  statsCards.value.find(c => c.key === "saved").value = savedJobIds.value.size;
  statsCards.value.find(c => c.key === "applied").value = appliedJobIds.value.size;
}

/* -------------------------------------------------------
   Recommended Jobs Tabs
------------------------------------------------------- */
function strongMatch(job) {
  const jobSkills = deriveJobSkills(job);
  const userSkills = userProfile.value.skills || [];
  return jobSkills.filter(s => userSkills.includes(s)).length >= 2;
}

const recommendedJobs = computed(() => jobs.value.filter(j => strongMatch(j)));

const tabs = computed(() => [
  { key: "all", label: "All Jobs" },
  { key: "recommended", label: "Recommended", count: recommendedJobs.value.length }
]);

/* -------------------------------------------------------
   Formatting Helpers
------------------------------------------------------- */
function formatExperience(exp) {
  const n = Number(exp);
  if (isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher";
  if (n === 1) return "1 year";
  return `${n} years`;
}

function relativeDate(dateStr) {
  if (!dateStr) return "Unknown";
  const d = new Date(dateStr);
  const diff = (Date.now() - d.getTime()) / (1000 * 3600 * 24);
  const days = Math.floor(diff);

  if (days <= 0) return "today";
  if (days === 1) return "1 day ago";
  if (days < 7) return `${days} days ago`;

  const weeks = Math.floor(days / 7);
  if (weeks < 4) return `${weeks} weeks ago`;

  const months = Math.floor(days / 30);
  return `${months} months ago`;
}

function formatReadableDate(raw) {
  if (!raw) return "Not specified";
  const d = new Date(raw);
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
}

function getShortDescription(desc) {
  if (!desc) return "No description.";
  let text = desc.replace(/[#*_`]/g, " ").replace(/\s+/g, " ").trim();
  return text.length <= 140 ? text : text.slice(0, 140) + "...";
}

/* -------------------------------------------------------
   Skill Extraction
------------------------------------------------------- */
function deriveJobSkills(job) {
  const txt = (job.description || "").toLowerCase();
  const detected = [];
  allSkills.value.forEach(skill => {
    if (txt.includes(skill.toLowerCase())) detected.push(skill);
  });
  return detected.length ? detected.slice(0, 6) : ["Communication", "Teamwork"];
}

/* -------------------------------------------------------
   Filtering & Sorting
------------------------------------------------------- */
const baseFilteredJobs = computed(() => {
  let list = [...jobs.value];

  if (activeTab.value === "recommended") {
    list = list.filter(j => strongMatch(j));
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(j =>
      (j.job_title || "").toLowerCase().includes(q) ||
      (j.location || "").toLowerCase().includes(q) ||
      (j.description || "").toLowerCase().includes(q)
    );
  }

  if (jobTypeFilter.value) list = list.filter(j => j.job_type === jobTypeFilter.value);

  if (experienceFilter.value !== "") {
    const minExp = Number(experienceFilter.value);
    list = list.filter(j => Number(j.experience) >= minExp);
  }

  if (locationFilter.value) {
    const loc = locationFilter.value.toLowerCase();
    list = list.filter(j => (j.location || "").toLowerCase().includes(loc));
  }

  if (selectedSkills.value.length) {
    list = list.filter(job =>
      selectedSkills.value.every(s => deriveJobSkills(job).includes(s))
    );
  }

  return list;
});

const filteredJobs = computed(() => {
  let list = [...baseFilteredJobs.value];

  switch (sortOption.value) {
    case "LATEST":
      list.sort((a, b) => (b.start_date || "").localeCompare(a.start_date || ""));
      break;
    case "EARLIEST":
      list.sort((a, b) => (a.start_date || "").localeCompare(b.start_date || ""));
      break;
    case "EXP_ASC":
      list.sort((a, b) => Number(a.experience) - Number(b.experience));
      break;
    case "EXP_DESC":
      list.sort((a, b) => Number(b.experience) - Number(a.experience));
      break;
  }

  return list;
});

const visibleJobs = computed(() => filteredJobs.value.slice(0, visibleCount.value));

function loadMore() {
  visibleCount.value += jobsPerPage;
}

function resetFilters() {
  searchQuery.value = "";
  jobTypeFilter.value = "";
  experienceFilter.value = "";
  locationFilter.value = "";
  sortOption.value = "LATEST";
  selectedSkills.value = [];
  activeTab.value = "all";
  visibleCount.value = jobsPerPage;
}

/* -------------------------------------------------------
   Save / Apply Jobs
   - We fetch saved/applied from server for canonical state
   - Save local copy only as a UI optimization
------------------------------------------------------- */
function isSaved(job) {
  return savedJobIds.value.has(job.job_id);
}

function isApplied(job) {
  return appliedJobIds.value.has(job.job_id);
}

async function toggleSave(job) {
  const token = localStorage.getItem("token");
  if (!token) {
    showInfoToast("Login required", "Please login to save jobs.");
    return;
  }

  try {
    if (isSaved(job)) {
      await fetch(`${API_BASE}/save-job/${job.job_id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
      });
      savedJobIds.value.delete(job.job_id);
      showInfoToast("Removed", "Job removed from saved.");
    } else {
      await fetch(`${API_BASE}/save-job`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ job_id: job.job_id })
      });
      savedJobIds.value.add(job.job_id);
      showSuccessToast("Saved", "Job added to saved list.");
    }
  } catch (err) {
    showErrorToast("Error", "Failed to update saved job.");
  }

  persistLocalState();
  refreshStats();
}

function persistLocalState() {
  try {
    const prefix = getUserKeyPrefix();
    localStorage.setItem(prefix + "candidate_saved_jobs", JSON.stringify([...savedJobIds.value]));
    localStorage.setItem(prefix + "candidate_applied_jobs", JSON.stringify([...appliedJobIds.value]));
  } catch {}
}

function restoreLocalState() {
  try {
    const prefix = getUserKeyPrefix();
    const saved = JSON.parse(localStorage.getItem(prefix + "candidate_saved_jobs") || "null");
    const applied = JSON.parse(localStorage.getItem(prefix + "candidate_applied_jobs") || "null");
    if (Array.isArray(saved)) savedJobIds.value = new Set(saved);
    if (Array.isArray(applied)) appliedJobIds.value = new Set(applied);
  } catch {}
}

/* -------------------------------------------------------
   Fetching Jobs & server-backed saved/applied lists
------------------------------------------------------- */
async function loadJobs() {
  loading.value = true;
  try {
    const res = await fetch(`${API_BASE}/jobs-all`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const data = await res.json();
    jobs.value = data.jobs || [];
  } catch {
    jobs.value = [];
    showErrorToast("Error", "Failed to fetch jobs.");
  } finally {
    loading.value = false;
    refreshStats();
  }
}

async function fetchSavedJobs() {
  try {
    const res = await fetch(`${API_BASE}/saved-jobs-details`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const data = await res.json();
    if (data.success && Array.isArray(data.jobs)) {
      // jobs from API may contain job_id as number or string
      savedJobIds.value = new Set(data.jobs.map(j => Number(j.job_id)));
      persistLocalState();
      refreshStats();
    }
  } catch {}
}

async function fetchAppliedJobs() {
  // canonical source of applied status
  try {
    const res = await fetch(`${API_BASE}/applied-jobs`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });
    const data = await res.json();
    if (data.success && Array.isArray(data.applications)) {
      appliedJobIds.value = new Set(data.applications.map(a => Number(a.job_id)));
      persistLocalState();
      refreshStats();
    }
  } catch (err) {
    // don't fail hard: keep local state if available
  }
}

/* -------------------------------------------------------
   Modal Setup
------------------------------------------------------- */
const jobDetailsModalRef = ref(null);
let jobDetailsModalInstance = null;

const credibilityModalRef = ref(null);
let credibilityModalInstance = null;

function openJobDetails(job) {
  selectedJob.value = { ...job };
  nextTick(() => jobDetailsModalInstance.show());
}

function closeJobDetails() {
  jobDetailsModalInstance.hide();
}

/* -------------------------------------------------------
   Job Description (Markdown)
------------------------------------------------------- */
const jobDescriptionHtml = computed(() =>
  selectedJob.value.description
    ? marked.parse(selectedJob.value.description)
    : "<p>No description available.</p>"
);

/* -------------------------------------------------------
   Credibility Test System (AUTO-APPLY mode)
------------------------------------------------------- */
const testJob = ref({});
const testQuestions = ref([]);
const currentQIndex = ref(0);
const answers = ref({});
const timeLeft = ref(0);
const testTimeLimit = ref(0);
const testLoading = ref(false);
const testInProgress = ref(false);
const testSubmitting = ref(false);
const showCorrect = ref(false);

let timer = null;

const currentQuestion = computed(() => testQuestions.value[currentQIndex.value] || { question: "", options: {} });

function sanitizeQuestion(str) {
  return String(str).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

const formatTimer = (s) => {
  s = Math.max(0, Math.floor(s));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
};

function clearTestState() {
  testQuestions.value = [];
  currentQIndex.value = 0;
  answers.value = {};
  timeLeft.value = 0;
  testInProgress.value = false;
  testSubmitting.value = false;
  showCorrect.value = false;
  if (timer) { clearInterval(timer); timer = null; }
}

async function onApplyClick(job) {
  if (isApplied(job)) {
    showInfoToast("Already applied", "You have applied for this job.");
    return;
  }

  if (testHistory[job.job_id]) {
    // In Auto-Apply mode we should not block if test done but not auto-applied,
    // however Option A means backend auto-applies. If backend hasn't, user can be allowed to re-apply:
    showInfoToast("Test done", "You already completed the test for this job.");
    return;
  }

  startCredibilityTest(job);
}

async function startCredibilityTest(job) {
  clearTestState();

  testJob.value = job;
  testLoading.value = true;

  nextTick(() => credibilityModalInstance.show());

  try {
    const res = await fetch(`${API_BASE}/credibility-test/${job.job_id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    });

    const data = await res.json();

    // Defensive: check structure
    if (!data || !Array.isArray(data.questions)) {
      testQuestions.value = [];
      testLoading.value = false;
      showErrorToast("Error", data.message || "No test available for this job.");
      return;
    }

    testQuestions.value = data.questions.map((q) => ({
      question: q.question,
      options: q.options,
      correct_option: q.correct_option
    }));

    timeLeft.value = data.time_limit || testQuestions.value.length * 30;
    testLoading.value = false;
    testInProgress.value = true;

    timer = setInterval(() => {
      timeLeft.value--;
      if (timeLeft.value <= 0) submitTest();
    }, 1000);

  } catch (err) {
    testLoading.value = false;
    showErrorToast("Error", "Failed to load test.");
  }
}

function selectOption(key) {
  if (showCorrect.value || !testInProgress.value) return;
  answers.value[currentQIndex.value] = key;
}

function prevQuestion() {
  if (currentQIndex.value > 0) currentQIndex.value--;
}

function nextQuestion() {
  if (currentQIndex.value < testQuestions.value.length - 1) currentQIndex.value++;
}

async function confirmSubmitTest() {
  submitTest();
}

async function submitTest() {
  if (testSubmitting.value) return;

  testSubmitting.value = true;
  testInProgress.value = false;
  showCorrect.value = true;

  let correct = 0;
  testQuestions.value.forEach((q, i) => {
    if ((answers.value[i] || "").toUpperCase() === (q.correct_option || "").toUpperCase()) {
      correct++;
    }
  });

  const score = Math.round((correct / (testQuestions.value.length || 1)) * 100);
  
  // When time ends
  if (timeLeft.value <= 0) {
    submitTest();  // modal closes ONLY after submit
  }

  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_BASE}/credibility-test/${testJob.value.job_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ score })
    });

    const data = await res.json();

    // Server returns:
    // { success: True, message: "...", score: score, status: "APPLIED" } when auto-applied
    // or success + status: "TEST_COMPLETED" (if backend doesn't auto-apply)
    if (data && data.success) {
      // If server confirmed APPLIED, reflect that in UI
      if (data.status === "APPLIED") {
        appliedJobIds.value.add(testJob.value.job_id);
      } else if (data.status === "TEST_COMPLETED") {
        // In Auto-Apply mode we prefer to attempt to call apply endpoint to ensure state
        try {
          const applyRes = await fetch(`${API_BASE}/job-apply`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ job_id: testJob.value.job_id })
          });
          const applyData = await applyRes.json();
          if (applyData && applyData.success) {
            appliedJobIds.value.add(testJob.value.job_id);
          }
        } catch {}
      }
    } else {
      // fallback: try apply endpoint (best effort)
      try {
        const fallback = await fetch(`${API_BASE}/job-apply`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ job_id: testJob.value.job_id })
        });
        const fallbackData = await fallback.json();
        if (fallbackData && fallbackData.success) {
          appliedJobIds.value.add(testJob.value.job_id);
        }
      } catch {}
    }

    // Mark test completed locally (so button shows "Test Done" briefly)
    testHistory[testJob.value.job_id] = true;

    persistLocalState();
    refreshStats();

    showSuccessToast("Test submitted", `Score: ${score}%`);
  } catch (err) {
    showErrorToast("Error", "Submission failed.");
  } finally {
    testSubmitting.value = false;
    // hide modal after a short delay
    setTimeout(() => {
      clearTestState();
      credibilityModalInstance.hide();
    }, 700);
  }
}

/* -------------------------------------------------------
   Avatar From Job Title
------------------------------------------------------- */
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
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&background=3864f2&color=fff&rounded=true`;
}

/* -------------------------------------------------------
   Skill Toggle
------------------------------------------------------- */
function toggleSkill(skill) {
  const idx = selectedSkills.value.indexOf(skill);
  if (idx >= 0) selectedSkills.value.splice(idx, 1);
  else selectedSkills.value.push(skill);
}

function clearSkills() {
  selectedSkills.value = [];
}

function setTab(key) {
  activeTab.value = key;
  visibleCount.value = jobsPerPage;
}

/* -------------------------------------------------------
   Chat (unchanged)
------------------------------------------------------- */
onMounted(async () => {
  restoreLocalState();
  await loadJobs();
  await Promise.all([fetchSavedJobs(), fetchAppliedJobs()]);

  refreshStats();
  nextTick(() => checkResumeStatusOnce());

  jobDetailsModalInstance = new Modal(jobDetailsModalRef.value, {
    backdrop: "static",
    keyboard: false
  });

  credibilityModalInstance = new Modal(credibilityModalRef.value, {
    backdrop: "static",
    keyboard: false
  });

  chatbotModalInstance = new Modal(chatbotModalRef.value)
});


function scrollChat() {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight;
    }
  });
}

async function openChatForJob(job) {
  chatbotJob.value = job;
  chatMessages.value = [{
    id: Date.now(),
    sender: "ai",
    text: `Hello! 👋<br/>Ask me anything about <b>${job.job_title}</b> at <b>${job.company}</b>.`
  }];
  botTyping.value = false;

  chatbotModalInstance.show();

  const token = localStorage.getItem("token");

  // Fetch Chat History
  try {
    const res = await fetch(`${API_BASE}/chatbot/history/${job.job_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();

    if (data.success && Array.isArray(data.history) && data.history.length) {
      chatMessages.value.push(...data.history.map((m, idx) => ({
            id: idx,
            sender: m.role === "user" ? "user" : "ai",
            text: m.content
          })
        )
      )
    } else {
      // First message
      chatMessages.value = [{
        id: Date.now(),
        sender: "ai",
        text: `Hello! 👋<br/>Ask me anything about <b>${job.job_title}</b> at <b>${job.company}</b>.`
      }];
    }

  } catch {
    chatMessages.value = [{
      id: Date.now(),
      sender: "ai",
      text: `Hello! 👋<br/>Ask me anything about <b>${job.job_title}</b> at <b>${job.company}</b>.`
    }];
  }

  scrollChat();
}


async function sendChatMsg() {
  if (!chatInput.value.trim()) return;

  // Push user message
  chatMessages.value.push({
    id: Date.now(),
    sender: "user",
    text: chatInput.value
  });

  const userQuery = chatInput.value;
  chatInput.value = "";
  scrollChat();

  botTyping.value = true;

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_BASE}/chatbot/response`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        job_id: chatbotJob.value.job_id,
        query: userQuery
      })
    });

    const data = await res.json();
    botTyping.value = false;

    if (data && data.success) {
      chatMessages.value.push({
        id: Date.now() + 1,
        sender: "ai",
        text: data.response
      });
    } else {
      chatMessages.value.push({
        id: Date.now() + 1,
        sender: "ai",
        text: "⚠️ Something went wrong, please try again."
      });
    }

  } catch (err) {
    botTyping.value = false;
    chatMessages.value.push({
      id: Date.now() + 1,
      sender: "ai",
      text: "⚠️ Server error, please try again."
    });
  }

  scrollChat();
}

async function clearChatConversation() {
  if (!chatbotJob.value) return;

  const confirm = await Swal.fire({
    title: "Clear Chat?",
    text: "This will permanently remove all conversation for this job.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, clear it",
    cancelButtonText: "Cancel"
  });

  if (!confirm.isConfirmed) return;

  const token = localStorage.getItem("token");

  try {
    await fetch(`${API_BASE}/chatbot/clear`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ job_id: chatbotJob.value.job_id })
    });

    // Reset local UI
    chatMessages.value = [
      {
        id: Date.now(),
        sender: "ai",
        text: `Chat reset. 👋<br/>Ask me anything about <b>${chatbotJob.value.job_title}</b> at <b>${chatbotJob.value.company}</b>.`
      }
    ];

    botTyping.value = false;
    scrollChat();

  } catch (err) {
    console.error(err);
    showErrorToast("Error", "Failed to clear chat.");
  }
}

</script>


<style scoped>
/* -------------------------------------------------------
   PAGE BACKGROUND
------------------------------------------------------- */
.candidate-dashboard-page {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #e2ecff, #f4f7ff 45%, #e9f1ff 80%);
}

.candidate-dashboard-section {
  min-height: calc(100vh - 70px);
  padding-bottom: 50px;
}

/* -------------------------------------------------------
   ANIMATIONS
------------------------------------------------------- */
.fade-in {
  opacity: 0;
  transform: translateY(16px);
  animation: fadeUp 0.6s ease forwards;
}

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* -------------------------------------------------------
   GLASS CARD GLOBAL
------------------------------------------------------- */
.glass-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  border: 1px solid rgba(207, 219, 240, 0.55);
  backdrop-filter: blur(14px);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.08);
  padding: 1.3rem 1.4rem;
}

/* -------------------------------------------------------
   STATS CARDS — Polished & Spaced
------------------------------------------------------- */
.stats-card {
  border-radius: 1.4rem;
  padding: 1.5rem 1.3rem !important;
  background: linear-gradient(135deg, #ffffff 0%, #eef2ff 100%);
  border: 1px solid rgba(160, 170, 190, 0.25);

  min-height: 135px;
  display: flex;
  gap: 14px;
  align-items: center;

  transition: 0.28s ease;
  cursor: pointer;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 22px 46px rgba(25, 40, 70, 0.22);
}

.stats-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: radial-gradient(circle, #0d6efd, #1d4ed8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.35rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
}

/* -------------------------------------------------------
   SEARCH BOX
------------------------------------------------------- */
.search-box {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
}

.search-box input {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* -------------------------------------------------------
   SKILL CHIPS
------------------------------------------------------- */
.skill-chip {
  padding: 6px 16px;
  font-size: 0.8rem;
  border-radius: 999px;
  background: white;
  border: 1px solid rgba(148, 163, 184, 0.35);
  cursor: pointer;
  transition: 0.2s;
}

.skill-chip:hover {
  background: rgba(0, 122, 255, 0.09);
}

.skill-chip-active {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff;
  border-color: transparent;
}

/* -------------------------------------------------------
   TABS (Pills)
------------------------------------------------------- */
.tab-pills .nav-link {
  border-radius: 999px;
  padding: 7px 18px;
  font-size: 0.87rem;
  color: #0d6efd;
  transition: 0.25s ease;
}

.tab-pills .nav-link.active {
  background: #0d6efd;
  color: #fff !important;
}

.tab-count {
  background: rgba(255, 255, 255, 0.4);
  color: #fff;
}

/* -------------------------------------------------------
   JOB CARDS — Premium Look
------------------------------------------------------- */
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

/* Bookmark Button */
.favorite-btn {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: 1px solid rgba(148,163,184,0.55);
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.25s ease;
  cursor: pointer;
}

.favorite-btn:hover {
  background: rgba(0,123,255,0.08);
}

.favorite-btn-active {
  background: #e0f2fe;
  border-color: transparent;
  color: #0284c7;
}

/* -------------------------------------------------------
   SKELETON LOADERS
------------------------------------------------------- */
.job-card-skeleton {
  border-radius: 1.5rem;
  padding: 1.5rem;
  background: #fff;
}

.skeleton-line {
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(90deg, #edf2ff 0%, #dfe7f3 50%, #edf2ff 100%);
  animation: shimmer 1.3s infinite linear;
}

.skeleton-pill {
  width: 60px;
  height: 18px;
  border-radius: 999px;
  background: linear-gradient(90deg, #edf2ff, #dfe7f3, #edf2ff);
  animation: shimmer 1.3s infinite linear;
}

.skeleton-pill-group {
  display: flex;
  gap: 6px;
}

@keyframes shimmer {
  0% { transform: translateX(-10%); }
  100% { transform: translateX(10%); }
}

/* -------------------------------------------------------
   GLASS MODALS
------------------------------------------------------- */
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
}

/* Correct / Incorrect Highlight */
.list-group-item-success {
  background: rgba(16,185,129,0.15) !important;
}
.list-group-item-danger {
  background: rgba(220,53,69,0.12) !important;
}

/* -------------------------------------------------------
   TOAST SYSTEM
------------------------------------------------------- */
/* -------------------------------------------------------
   CLEAN MINIMAL TOAST SYSTEM
------------------------------------------------------- */
.toast-top-right {
  position: fixed;
  top: 22px;
  right: 22px;
  z-index: 1200;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.neo-toast {
  pointer-events: auto;

  display: flex;
  align-items: center;
  gap: 10px;

  padding: 10px 16px;
  border-radius: 12px;

  background: #ffffff;
  border: 1px solid rgba(220, 227, 240, 0.6);

  font-size: 0.85rem;
  color: #334155;

  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);

  /* Compact Single-Line */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  /* Animation */
  opacity: 0;
  transform: translateY(-8px);
  animation: toastSlideIn 0.35s ease forwards;
}

/* Toast types (simple colored bar on left) */
.neo-toast-success {
  border-left: 4px solid #16a34a;
}
.neo-toast-error {
  border-left: 4px solid #dc2626;
}
.neo-toast-info {
  border-left: 4px solid #2563eb;
}

/* Slide + fade in */
@keyframes toastSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Icon style */
.neo-toast-left {
  font-size: 1.1rem;
  color: #1e293b;
  display: flex;
  align-items: center;
}

/* Title + message merged into one line */
.neo-toast-body {
  display: flex;
  align-items: center;
  gap: 6px;
}

.neo-toast-title {
  font-weight: 600;
}

.neo-toast-msg {
  opacity: 0.85;
}

/* Remove close button entirely */
.neo-toast-close {
  display: none !important;
}

/* Chatbot button */
.chat-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #eef4ff;
  border: 1px solid rgba(140, 160, 200, 0.5);
  color: #1e3a8a;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.25s ease;
}

.chat-btn:hover {
  background: #dbe8ff;
  transform: translateY(-2px);
}

/* ---------------------------------------------------
    CHATBOT FIX: MODERN, CENTERED, CLEAN UI
--------------------------------------------------- */

/* Center modal properly + add shadow */
#jobChatbotModal .modal-dialog {
  max-width: 650px;
  margin: auto;
  padding: 0;
}

.chatbot-wrapper {
  width: 100%;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  overflow: hidden;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.25);
  animation: chatFadeUp 0.4s ease;
}

@keyframes chatFadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* HEADER */
.chatbot-header {
  padding: 18px 22px;
  background: #f1f5ff;
  border-bottom: 1px solid #dce3ff;
  display: flex;
  align-items: center;
}

.bot-avatar {
  width: 50px;
  height: 50px;
  background: #dbeafe;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #1e3a8a;
  font-size: 1.6rem;
}

/* CHAT BODY */
.chatbot-body {
  padding: 22px;
  height: 420px;
  overflow-y: auto;
  background: #f8fafc;
  scrollbar-width: thin;
}

/* AI & USER MESSAGE BUBBLES */
.msg {
  display: flex;
  margin-bottom: 16px;
}

.msg-ai {
  justify-content: flex-start;
}

.msg-user {
  justify-content: flex-end;
}

.bubble {
  max-width: 75%;
  padding: 12px 16px;
  font-size: 0.92rem;
  line-height: 1.5;
  border-radius: 16px;
}

.msg-ai .bubble {
  background: white;
  border: 1px solid #dbe0eb;
  color: #1e293b;
}

.msg-user .bubble {
  background: #dbeafe;
  color: #1e3a8a;
}

/* TYPING DOTS */
.typing-indicator {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #a0aec0;
  border-radius: 50%;
  animation: typingBlink 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: .2s; }
.typing-indicator span:nth-child(3) { animation-delay: .4s; }

@keyframes typingBlink {
  0% { opacity: .3; transform: translateY(0); }
  20% { opacity: 1; transform: translateY(-4px); }
  100% { opacity: .3; transform: translateY(0); }
}

/* INPUT BAR */
.chatbot-input {
  padding: 14px 18px;
  background: white;
  border-top: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chatbot-input input {
  flex: 1;
  height: 45px;
  border-radius: 12px;
  border: 1px solid #cfd8e3;
  padding-left: 16px;
  font-size: 0.95rem;
  outline: none;
}

.chatbot-input input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.20);
}

.chatbot-input button {
  height: 45px;
  width: 55px;
  border-radius: 12px;
  background: linear-gradient(90deg, #4f46e5, #3b82f6);
  border: none;
  color: white;
  font-size: 1.3rem;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.25s ease;
}

.chatbot-input button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59,130,246,0.4);
}

.chatbot-header button {
  font-size: 0.75rem;
  padding: 4px 10px;
}


</style>
