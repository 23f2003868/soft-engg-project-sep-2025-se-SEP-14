<template>
  <div class="saved-jobs-page">

    <!-- NAVBAR -->
    <CandidateNavbar />

    <!-- TOASTS (Same as Dashboard) -->
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
          </div>
        </div>
      </div>
    </div>

    <!-- MAIN -->
    <section class="saved-section py-4 py-md-5">
      <div class="container">

        <!-- HEADER -->
        <div class="mb-4 fade-in visible">
          <h3 class="fw-bold text-primary mb-1">Saved Jobs</h3>
          <p class="text-muted small">Jobs you saved for later review.</p>
        </div>

        <!-- LOADING -->
        <div v-if="loading" class="row g-4 mt-2">
          <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
            <div class="job-card-skeleton glass-card p-4"></div>
          </div>
        </div>

        <!-- SAVED JOB LIST -->
        <div v-else>
          <div v-if="savedJobs.length" class="row g-4 fade-in visible">

            <div
              v-for="job in savedJobs"
              :key="job.job_id"
              class="col-md-6 col-lg-4"
            >
              <div class="job-card glass-card p-4 d-flex flex-column h-100">

                <!-- HEADER -->
                <div class="d-flex justify-content-between align-items-start mb-3">

                  <div class="d-flex gap-3 align-items-start">

                    <div class="job-avatar">
                      <img :src="generateJobAvatar(job.job_title)" />
                    </div>

                    <div>
                      <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>

                      <div class="small text-primary fw-semibold mb-1">
                        <i class="bi bi-building me-1"></i>
                        {{ job.company || "Unknown Company" }}
                      </div>

                      <div class="small text-muted">
                        <i class="bi bi-geo-alt me-1 text-primary"></i>
                        {{ job.location || "Not specified" }}
                      </div>
                    </div>
                  </div>

                  <button
                    class="btn btn-sm rounded-circle favorite-btn favorite-btn-active"
                    @click="unsaveJob(job)"
                    title="Remove from saved"
                  >
                    <i class="bi bi-bookmark-fill"></i>
                  </button>

                </div>

                <!-- META -->
                <div class="small text-muted mb-1">
                  <i class="bi bi-briefcase me-1 text-primary"></i>
                  {{ job.job_type }}
                  •
                  <i class="bi bi-clock-history ms-1 me-1 text-primary"></i>
                  {{ relativeDate(job.start_date) }}
                </div>

                <div class="small text-muted mb-1">
                  <i class="bi bi-person-workspace me-1 text-primary"></i>
                  Experience:
                  <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
                </div>

                <div class="small text-muted mb-2">
                  <i class="bi bi-calendar-event me-1 text-primary"></i>
                  End Date:
                  {{ formatReadableDate(job.end_date) }}
                </div>

                <!-- DESCRIPTION -->
                <p class="job-snippet text-secondary small mt-2 mb-3">
                  {{ getShortDescription(job.description) }}
                </p>

                <!-- SKILLS -->
                <div class="mb-3 d-flex flex-wrap gap-1">
                  <span
                    v-for="skill in deriveJobSkills(job)"
                    :key="skill"
                    class="badge rounded-pill bg-light text-primary border small-pill"
                  >
                    {{ skill }}
                  </span>
                </div>

                <!-- ACTION BUTTONS -->
                <div class="d-flex justify-content-between align-items-center mt-auto">

                  <button
                    class="btn btn-sm btn-outline-primary rounded-pill"
                    @click="openJobModal(job)"
                  >
                    View Details
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

          <!-- EMPTY -->
          <div v-else class="text-center text-muted mt-5 fade-in visible">
            <i class="bi bi-bookmark fs-1 text-secondary d-block mb-3"></i>
            <p>You haven’t saved any jobs yet.</p>
          </div>
        </div>

      </div>
    </section>

    <!-- JOB DETAILS MODAL -->
    <div class="modal fade" id="savedJobModal" tabindex="-1" ref="savedJobModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">

          <div class="modal-header border-0">
            <div>
              <h5 class="modal-title fw-bold">{{ selectedJob.job_title }}</h5>
              <p class="small text-muted mb-0">
                <i class="bi bi-geo-alt me-1 text-primary"></i>
                {{ selectedJob.location }}
              </p>
              <p class="small text-muted mb-0">
                <i class="bi bi-person-workspace me-1 text-primary"></i>
                Experience: {{ formatExperience(selectedJob.experience) }}
              </p>
              <p class="small text-muted mb-0">
                <i class="bi bi-calendar-event me-1 text-primary"></i>
                End Date: {{ formatReadableDate(selectedJob.end_date) }}
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
                v-for="skill in deriveJobSkills(selectedJob)"
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

    <!-- CREDIBILITY TEST MODAL -->
    <div class="modal fade" id="credibilityTestModal" tabindex="-1" ref="credibilityModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">

          <div class="modal-header border-0">
            <h5 class="modal-title fw-bold">Credibility Test</h5>
            <button type="button" class="btn-close" @click="cancelTest"></button>
          </div>

          <div class="modal-body">

            <div v-if="testJob">
              <p class="small text-muted">Job:
                <strong>{{ testJob.job_title }}</strong>
              </p>
            </div>

            <div class="d-flex justify-content-between mb-2">
              <div>
                <small class="text-muted">Question</small>
                <div class="fw-semibold">#{{ currentQIndex + 1 }} / {{ testQuestions.length }}</div>
              </div>
              <div>
                <small class="text-muted">Time left</small>
                <div class="fw-semibold">{{ formatTimer(timeLeft) }}</div>
              </div>
            </div>

            <hr />

            <div v-if="testLoading" class="text-center py-4">
              <div class="spinner-border text-primary"></div>
            </div>

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
                    'list-group-item-danger': showCorrect && answers[currentQIndex] === key && currentQuestion.correct_option !== key
                  }"
                  :disabled="showCorrect"
                  @click="selectOption(key)"
                >
                  <strong>{{ key }}.</strong>
                  <span v-html="sanitizeQuestion(opt)"></span>
                </button>
              </div>

              <div class="d-flex justify-content-between mt-3">
                <button
                  class="btn btn-sm btn-outline-secondary rounded-pill"
                  :disabled="currentQIndex === 0"
                  @click="prevQuestion"
                >Previous</button>

                <button
                  class="btn btn-sm btn-outline-secondary rounded-pill"
                  :disabled="currentQIndex >= testQuestions.length - 1"
                  @click="nextQuestion"
                >Next</button>

                <button
                  class="btn btn-sm btn-danger rounded-pill"
                  @click="cancelTest"
                >Cancel</button>

                <button
                  class="btn btn-sm btn-success rounded-pill"
                  @click="confirmSubmitTest"
                >Submit Test</button>
              </div>

            </div>

            <div v-else class="text-center py-4">No test available.</div>

          </div>

        </div>
      </div>
    </div>

    <FloatingChatBot />
  </div>
</template>


<script setup>
/* -------------------------------------------------------
   Imports
------------------------------------------------------- */
import { ref, reactive, computed, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import CandidateNavbar from "../components/CandidateNavbar.vue";
import FloatingChatBot from "../components/ChatBot.vue";
import { marked } from "marked";

/* -------------------------------------------------------
   API + Base State
------------------------------------------------------- */
const API_BASE = "http://127.0.0.1:5000/api";

const savedJobs = ref([]);
const appliedJobIds = ref(new Set());
const testHistory = reactive({});
const loading = ref(true);

const selectedJob = ref({});
const testJob = ref({});

/* -------------------------------------------------------
   Toast System (Same as Dashboard)
------------------------------------------------------- */
const toasts = ref([]);
let toastCounter = 1;
const toastTimers = new Map();

function nextToastId() {
  return `toast-${Date.now()}-${toastCounter++}`;
}

function showToast({ type = "info", title = "", message = "", duration = 4000 }) {
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
    createdAt: Date.now()
  };

  toasts.value.unshift(toast);
  scheduleRemoval(toast.id, duration);
}

const showSuccessToast = (title, msg) =>
  showToast({ type: "success", title, message: msg });

const showErrorToast = (title, msg) =>
  showToast({ type: "error", title, message: msg, duration: 0 });

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
  toasts.value = toasts.value.filter((t) => t.id !== id);
  clearTimer(id);
}

/* -------------------------------------------------------
   Utils
------------------------------------------------------- */
function formatExperience(exp) {
  const n = Number(exp);
  if (isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher";
  if (n === 1) return "1 year";
  return `${n} years`;
}

function formatReadableDate(raw) {
  if (!raw) return "Not specified";
  const d = new Date(raw);
  return d.toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
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

function getShortDescription(desc) {
  if (!desc) return "No description.";
  let text = desc.replace(/[#*_`]/g, " ").replace(/\s+/g, " ").trim();
  return text.length <= 140 ? text : text.slice(0, 140) + "...";
}

function deriveJobSkills(job) {
  const txt = (job.description || "").toLowerCase();
  const skills = ["Python", "SQL", "VueJS", "JavaScript", "React", "Node.js", "Flask", "Django"];
  return skills.filter((s) => txt.includes(s.toLowerCase())).slice(0, 6);
}

/* Avatar */
function getInitials(title) {
  if (!title) return "JD";
  const parts = title.trim().split(" ");
  if (parts.length === 1) {
    return (parts[0][0] + (parts[0][1] || "D")).toUpperCase();
  }
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

function generateJobAvatar(title) {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(
    getInitials(title)
  )}&background=3864f2&color=fff&rounded=true`;
}

/* -------------------------------------------------------
   Load saved + applied jobs
------------------------------------------------------- */
async function loadAll() {
  const token = localStorage.getItem("token");

  try {
    const res1 = await fetch(`${API_BASE}/saved-jobs-details`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data1 = await res1.json();
    savedJobs.value = data1.jobs || [];

    const res2 = await fetch(`${API_BASE}/applied-jobs`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data2 = await res2.json();

    appliedJobIds.value = new Set(data2.applications?.map((a) => a.job_id) || []);

  } catch (e) {
    console.log(e);
  }

  loading.value = false;
}

function isApplied(job) {
  return appliedJobIds.value.has(job.job_id);
}

async function unsaveJob(job) {
  const token = localStorage.getItem("token");

  try {
    await fetch(`${API_BASE}/save-job/${job.job_id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });

    savedJobs.value = savedJobs.value.filter((j) => j.job_id !== job.job_id);

    showToast({
      type: "info",
      title: "Removed",
      message: "Job removed from saved list."
    });

  } catch {
    showErrorToast("Error", "Could not remove saved job.");
  }
}

/* -------------------------------------------------------
   Job modal
------------------------------------------------------- */
const savedJobModalRef = ref(null);
let savedModal = null;

const jobMarkdownHtml = computed(() =>
  selectedJob.value.description
    ? marked.parse(selectedJob.value.description)
    : "<p>No description available.</p>"
);

function openJobModal(job) {
  selectedJob.value = job;
  savedModal.show();
}

/* -------------------------------------------------------
   Credibility Test System (FULL copy from Dashboard)
------------------------------------------------------- */
const credibilityModalRef = ref(null);
let credibilityModalInstance = null;

const testQuestions = ref([]);
const currentQIndex = ref(0);
const answers = ref({});
const timeLeft = ref(0);
const testLoading = ref(false);
const testInProgress = ref(false);
const testSubmitting = ref(false);
const showCorrect = ref(false);

let timer = null;

const currentQuestion = computed(() =>
  testQuestions.value[currentQIndex.value] || { question: "", options: {} }
);

function sanitizeQuestion(str) {
  return String(str).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function formatTimer(sec) {
  sec = Math.max(0, Math.floor(sec));
  return `${String(Math.floor(sec / 60)).padStart(2, "0")}:${String(sec % 60).padStart(2, "0")}`;
}

function clearTestState() {
  testQuestions.value = [];
  currentQIndex.value = 0;
  answers.value = {};
  timeLeft.value = 0;
  testInProgress.value = false;
  testSubmitting.value = false;
  showCorrect.value = false;
  if (timer) clearInterval(timer);
}

async function onApplyClick(job) {
  if (isApplied(job)) {
    showToast({ type: "info", title: "Applied", message: "You already applied." });
    return;
  }

  if (testHistory[job.job_id]) {
    showToast({ type: "info", title: "Test Done", message: "You already completed the test." });
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

  } catch {
    showErrorToast("Error", "Failed to load test.");
    testLoading.value = false;
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
    if ((answers.value[i] || "").toUpperCase() === q.correct_option.toUpperCase()) {
      correct++;
    }
  });

  const score = Math.round((correct / testQuestions.value.length) * 100);

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

    // Guarantee applied
    appliedJobIds.value.add(testJob.value.job_id);
    testHistory[testJob.value.job_id] = true;

    showSuccessToast("Test submitted", `Score: ${score}%`);

  } catch {
    showErrorToast("Error", "Submission failed.");
  }

  setTimeout(() => credibilityModalInstance.hide(), 800);
}

function cancelTest() {
  clearTestState();
  credibilityModalInstance.hide();
}

/* -------------------------------------------------------
   Lifecycle
------------------------------------------------------- */
onMounted(async () => {
  await loadAll();

  savedModal = new Modal(savedJobModalRef.value);
  credibilityModalInstance = new Modal(credibilityModalRef.value, {
    backdrop: "static",
    keyboard: false
  });
});
</script>


<style scoped>
/* -------------------------------------------------------
   SAME UI STYLES FROM DASHBOARD
------------------------------------------------------- */

/* Background */
.saved-jobs-page {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #e2ecff, #f4f7ff 45%, #e9f1ff 80%);
}

/* Glass Card */
.glass-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  border: 1px solid rgba(207, 219, 240, 0.55);
  backdrop-filter: blur(14px);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.08);
  padding: 1.3rem 1.4rem;
}

/* Job Card (Exact Dashboard Style) */
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

/* Snippet */
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
.favorite-btn-active {
  background: #e0f2fe;
  border-color: transparent;
  color: #0284c7;
}

/* Skeleton */
.job-card-skeleton {
  border-radius: 1.5rem;
  padding: 1.5rem;
  background: #fff;
}

/* Modal Glass */
.glass-modal {
  background: rgba(255, 255, 255, 0.96);
  border-radius: 1.4rem;
  backdrop-filter: blur(20px);
}

/* Scroll */
.modal-body::-webkit-scrollbar {
  width: 6px;
}
.modal-body::-webkit-scrollbar-thumb {
  background: #c7d4ff;
  border-radius: 10px;
}

/* Toast System (Same as Dashboard) */
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
  opacity: 0;
  transform: translateY(-8px);
  animation: toastSlideIn 0.35s ease forwards;
}

.neo-toast-success { border-left: 4px solid #16a34a; }
.neo-toast-error { border-left: 4px solid #dc2626; }
.neo-toast-info { border-left: 4px solid #2563eb; }

@keyframes toastSlideIn {
  from { opacity: 0; transform: translateY(-10px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
