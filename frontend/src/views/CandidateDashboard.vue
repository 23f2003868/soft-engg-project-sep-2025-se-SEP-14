<template>
  <div class="candidate-dashboard-page">
    <CandidateNavbar />

    <section class="candidate-dashboard-section py-4 py-md-5">
      <div class="container">

        <!-- HEADER + STATS -->
        <div class="row align-items-center mb-4 mb-md-5 fade-in visible">
          <div class="col-md-7">
            <p class="text-muted small mb-1">Candidate Dashboard</p>
            <h2 class="fw-bold text-primary mb-1">
              Welcome, {{ userProfile.name || "Candidate" }}
            </h2>
            <p class="text-secondary mb-0">
              Discover opportunities tailored to your skills and experience.
            </p>
          </div>

          <!-- Stats cards -->
          <div class="col-md-5 mt-3 mt-md-0">
            <div class="row g-2 g-md-3">
              <div class="col-4" v-for="card in statsCards" :key="card.key">
                <div class="stats-card d-flex align-items-center p-2 p-md-3 h-100">
                  <div class="stats-icon me-2">
                    <i :class="['bi', card.icon]"></i>
                  </div>
                  <div class="stats-text text-start">
                    <div class="stats-label small text-muted">
                      {{ card.label }}
                    </div>
                    <div class="stats-value fw-bold fs-6">
                      {{ card.value }}
                    </div>
                    <!-- subtitle removed as per instruction -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FILTERS + SEARCH BAR -->
        <div class="filter-card glass-card p-3 p-md-4 mb-4 fade-in visible">
          <div class="row g-3 align-items-center">

            <!-- SEARCH -->
            <div class="col-lg-4">
              <label class="form-label small text-muted mb-1">Search</label>
              <div class="input-group search-box">
                <span class="input-group-text border-0 bg-transparent">
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

            <!-- JOB TYPE -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Job Type</label>
              <select v-model="jobTypeFilter" class="form-select form-select-sm rounded-3">
                <option value="">All</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <!-- EXPERIENCE -->
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

            <!-- LOCATION QUICK FILTER -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Location quick filter</label>
              <select v-model="locationFilter" class="form-select form-select-sm rounded-3">
                <option value="">Anywhere</option>
                <option v-for="loc in popularLocations" :key="loc" :value="loc">
                  {{ loc }}
                </option>
              </select>
            </div>

            <!-- SORT -->
            <div class="col-6 col-lg-2">
              <label class="form-label small text-muted mb-1">Sort By</label>
              <select v-model="sortOption" class="form-select form-select-sm rounded-3">
                <option value="LATEST">Latest</option>
                <option value="EARLIEST">Oldest</option>
                <option value="EXP_ASC">Experience: Low to High</option>
                <option value="EXP_DESC">Experience: High to Low</option>
              </select>
            </div>

          </div>

          <!-- SKILL CHIPS -->
          <div class="mt-3 d-flex flex-wrap align-items-center gap-2">
            <span class="small text-muted me-1">Filter by skills:</span>
            <button
              v-for="skill in allSkills"
              :key="skill"
              type="button"
              class="btn btn-sm skill-chip"
              :class="{
                'skill-chip-active': selectedSkills.includes(skill)
              }"
              @click="toggleSkill(skill)"
            >
              {{ skill }}
            </button>

            <button
              v-if="selectedSkills.length"
              type="button"
              class="btn btn-sm btn-link text-decoration-none ms-1"
              @click="clearSkills"
            >
              Clear skills
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
              <span v-if="tab.count !== undefined" class="badge rounded-pill ms-1 tab-count">
                {{ tab.count }}
              </span>
            </button>
          </li>
        </ul>

        <!-- JOB GRID -->
        <div v-if="loading" class="row g-4">
          <!-- Skeleton loaders -->
          <div v-for="n in 6" :key="n" class="col-md-6 col-lg-4">
            <div class="job-card-skeleton glass-card p-4">
              <div class="skeleton-line w-50 mb-2"></div>
              <div class="skeleton-line w-25 mb-3"></div>
              <div class="skeleton-line w-75 mb-2"></div>
              <div class="skeleton-line w-50 mb-2"></div>
              <div class="skeleton-pill-group mt-3">
                <span class="skeleton-pill"></span>
                <span class="skeleton-pill"></span>
                <span class="skeleton-pill"></span>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <div v-if="visibleJobs.length" class="row g-4 fade-in visible">
            <div
              v-for="job in visibleJobs"
              :key="job.job_id"
              class="col-md-6 col-lg-4"
            >
              <div class="job-card glass-card p-4 h-100 d-flex flex-column">

                <!-- TOP ROW: TITLE + MATCH BADGE -->
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h5 class="fw-bold text-dark mb-1">
                      {{ job.job_title }}
                    </h5>
                    <div class="small text-muted">
                      <i class="bi bi-geo-alt me-1 text-primary"></i>
                      {{ job.location || "Location not specified" }}
                    </div>
                  </div>

                  <span
                    v-if="strongMatch(job)"
                    class="badge rounded-pill bg-success-subtle text-success fw-semibold small-pill"
                  >
                    Strong match
                  </span>
                </div>

                <!-- META INFO (tighter spacing + end date) -->
                <div class="small text-muted mb-1">
                  <span class="me-2">
                    <i class="bi bi-briefcase me-1 text-primary"></i>
                    {{ job.job_type || "Job type N/A" }}
                  </span>
                  <span>
                    <i class="bi bi-clock-history me-1 text-primary"></i>
                    Posted {{ relativeDate(job.start_date) }}
                  </span>
                </div>

                <div class="small text-muted mb-1">
                  <i class="bi bi-person-workspace me-1 text-primary"></i>
                  Experience:
                  <span class="fw-semibold">
                    {{ formatExperience(job.experience) }}
                  </span>
                </div>

                <div class="small text-muted mb-2">
                  <i class="bi bi-calendar-event me-1 text-primary"></i>
                  End Date:
                  <span class="fw-semibold">
                    {{ formatReadableDate(job.end_date) }}
                  </span>
                </div>

                <!-- DESCRIPTION SNIPPET -->
                <p class="job-snippet text-secondary small flex-grow-1">
                  {{ getShortDescription(job.description) }}
                </p>

                <!-- SKILL CHIPS (from description/guess) -->
                <div class="mb-3 d-flex flex-wrap gap-1">
                  <span
                    v-for="skill in deriveJobSkills(job)"
                    :key="skill"
                    class="badge rounded-pill bg-light text-primary border small-pill"
                  >
                    {{ skill }}
                  </span>
                </div>

                <!-- ACTION ROW -->
                <div class="d-flex justify-content-between align-items-center mt-2">
                  <button
                    class="btn btn-sm btn-outline-primary rounded-pill"
                    @click="openJobDetails(job)"
                    data-bs-toggle="modal"
                    data-bs-target="#jobDetailsModal"
                  >
                    View Details
                  </button>

                  <div class="d-flex align-items-center gap-2">
                    <!-- Save / Unsave -->
                    <button
                      class="btn btn-sm rounded-circle favorite-btn"
                      :class="{ 'favorite-btn-active': isSaved(job) }"
                      @click="toggleSave(job)"
                      :title="isSaved(job) ? 'Unsave job' : 'Save job'"
                    >
                      <i :class="isSaved(job) ? 'bi bi-bookmark-fill' : 'bi bi-bookmark'"></i>
                    </button>

                    <!-- Apply just shows "coming soon" modal -->
                    <button
                      class="btn btn-sm btn-success rounded-pill"
                      @click="openApplyComingSoon(job)"
                    >
                      Apply
                    </button>
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- NO JOBS STATE -->
          <div
            v-else
            class="text-center text-muted mt-5 fade-in visible"
          >
            <i class="bi bi-briefcase fs-1 text-secondary d-block mb-3"></i>
            <p class="mb-1">No jobs match your current filters.</p>
            <p class="small">
              Try clearing some filters or switching the tab.
            </p>
            <button class="btn btn-outline-primary rounded-pill btn-sm mt-2" @click="resetFilters">
              Reset filters
            </button>
          </div>

          <!-- LOAD MORE -->
          <div
            v-if="!loading && filteredJobs.length > jobsPerPage"
            class="d-flex justify-content-center mt-4"
          >
            <button
              class="btn btn-outline-secondary rounded-pill btn-sm"
              v-if="visibleCount < filteredJobs.length"
              @click="loadMore"
            >
              Load more jobs
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- JOB DETAILS MODAL -->
    <div
      class="modal fade"
      id="jobDetailsModal"
      tabindex="-1"
      aria-labelledby="jobDetailsModalLabel"
      aria-hidden="true"
      ref="jobDetailsModalRef"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header border-0">
            <div>
              <h5 class="modal-title fw-bold" id="jobDetailsModalLabel">
                {{ selectedJob?.job_title }}
              </h5>
              <p class="small text-muted mb-0">
                <i class="bi bi-geo-alt me-1 text-primary"></i>
                {{ selectedJob?.location }} •
                <i class="bi bi-briefcase ms-2 me-1 text-primary"></i>
                {{ selectedJob?.job_type }}
              </p>
              <p class="small text-muted mb-0">
                Experience:
                <span class="fw-semibold">
                  {{ formatExperience(selectedJob?.experience) }}
                </span>
              </p>
              <p class="small text-muted mb-0">
                End Date:
                <span class="fw-semibold">
                  {{ formatReadableDate(selectedJob?.end_date) }}
                </span>
              </p>
            </div>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body pt-0">
            <hr class="mt-0 mb-3" />
            <h6 class="fw-semibold text-primary mb-2">Job Description</h6>

            <!-- FULL MARKDOWN DESCRIPTION -->
            <div
              class="small text-secondary mb-3 markdown-body"
              v-html="jobDescriptionHtml"
            ></div>

            <h6 class="fw-semibold text-primary mb-2">Skills Highlight</h6>
            <div class="mb-3 d-flex flex-wrap gap-1">
              <span
                v-for="skill in deriveJobSkills(selectedJob || {})"
                :key="skill"
                class="badge rounded-pill bg-light text-primary border small-pill"
              >
                {{ skill }}
              </span>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-2">
              <button
                class="btn btn-outline-primary btn-sm rounded-pill"
                @click="toggleSave(selectedJob)"
              >
                <i :class="isSaved(selectedJob) ? 'bi bi-bookmark-fill me-1' : 'bi bi-bookmark me-1'"></i>
                {{ isSaved(selectedJob) ? "Saved" : "Save Job" }}
              </button>

              <button
                v-if="selectedJob"
                class="btn btn-success btn-sm rounded-pill"
                data-bs-dismiss="modal"
                @click="openApplyComingSoon(selectedJob)"
              >
                Apply
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SIMPLE "COMING SOON" APPLY MODAL -->
    <div
      class="modal fade"
      id="applyComingSoonModal"
      tabindex="-1"
      aria-hidden="true"
      ref="applyModalRef"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-modal border-0">
          <div class="modal-header border-0">
            <h5 class="modal-title fw-bold">
              Application coming soon
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p class="small text-muted mb-2">
              You clicked apply for:
            </p>
            <p class="fw-semibold mb-2">
              {{ jobForApply?.job_title || "Selected job" }}
            </p>
            <p class="small text-secondary mb-0">
              The full online application flow is not live yet.
              For now, you can save this job and come back later.
            </p>
          </div>
          <div class="modal-footer border-0">
            <button
              type="button"
              class="btn btn-sm btn-outline-primary rounded-pill"
              data-bs-dismiss="modal"
            >
              Okay
            </button>
          </div>
        </div>
      </div>
    </div>

    <FloatingChatBot />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import { marked } from "marked";

import CandidateNavbar from "../components/CandidateNavbar.vue";
import FloatingChatBot from "../components/ChatBot.vue";

// -------------------------------
// BASIC STATE
// -------------------------------
const API_BASE = "http://127.0.0.1:5000/api";

const jobs = ref([]);
const loading = ref(false);
const selectedJob = ref(null);

// Tabs: all, recommended, applied, saved
const activeTab = ref("all");

const searchQuery = ref("");
const jobTypeFilter = ref("");
const experienceFilter = ref("");
const locationFilter = ref("");
const sortOption = ref("LATEST");

const selectedSkills = ref([]);

const visibleCount = ref(9);
const jobsPerPage = 9;

// Saved / Applied jobs – tracked locally + synced with backend for saved
const savedJobIds = ref(new Set());
const appliedJobIds = ref(new Set());

const popularLocations = ref([
  "Bangalore",
  "Chennai",
  "Hyderabad",
  "Pune",
  "Delhi NCR",
]);

// Very simple skills dictionary (used to derive from job description text)
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
  "Data Analysis",
]);

// User profile (name from localStorage for now)
const userProfile = ref({
  name: localStorage.getItem("firstname") || "Candidate",
  skills: ["Python", "SQL", "VueJS"], // can be dynamic later
});

// Stats cards
const statsCards = ref([
  {
    key: "total",
    label: "Total Jobs",
    value: 0,
    icon: "bi-briefcase-fill",
  },
  {
    key: "saved",
    label: "Saved Jobs",
    value: 0,
    icon: "bi-bookmark-heart-fill",
  },
  {
    key: "applied",
    label: "Applied",
    value: 0,
    icon: "bi-send-check-fill",
  },
]);

// Tabs with counters
const tabs = computed(() => [
  { key: "all", label: "All Jobs" },
  { key: "recommended", label: "Recommended", count: recommendedJobs.value.length },
]);

// -------------------------------
// UTIL HELPERS
// -------------------------------
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

  return d.toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

// small plain text from markdown for card
const getShortDescription = (desc) => {
  if (!desc) return "No description available.";

  let plain = String(desc);

  // Strip markdown headings, bullets, emphasis, code markers, etc.
  plain = plain
    .replace(/[#*_`>-]/g, " ")
    .replace(/\[(.*?)\]\((.*?)\)/g, "$1") // links
    .replace(/\s+/g, " ")
    .trim();

  if (!plain.length) return "No description available.";

  if (plain.length <= 140) return plain;
  return plain.slice(0, 140) + "...";
};

const deriveJobSkills = (job) => {
  if (!job) return [];
  const text = (job.description || "").toLowerCase();
  const skillsSet = new Set();

  allSkills.value.forEach((skill) => {
    if (text.includes(skill.toLowerCase())) {
      skillsSet.add(skill);
    }
  });

  // If none detected, return a couple of generic tags
  if (skillsSet.size === 0) {
    return ["Communication", "Teamwork"];
  }

  return Array.from(skillsSet).slice(0, 6);
};

const strongMatch = (job) => {
  if (!job) return false;
  const jobSkills = deriveJobSkills(job);
  if (!jobSkills.length) return false;

  const candidateSkills = userProfile.value.skills || [];
  if (!candidateSkills.length) return false;

  const intersection = jobSkills.filter((s) => candidateSkills.includes(s));
  return intersection.length >= 2; // simple heuristic
};

// Markdown HTML for modal
const jobDescriptionHtml = computed(() => {
  if (!selectedJob.value || !selectedJob.value.description) {
    return "<p>No detailed description available.</p>";
  }
  return marked.parse(String(selectedJob.value.description));
});

// -------------------------------
// FILTERS / SORTING
// -------------------------------
const toggleSkill = (skill) => {
  const idx = selectedSkills.value.indexOf(skill);
  if (idx >= 0) {
    selectedSkills.value.splice(idx, 1);
  } else {
    selectedSkills.value.push(skill);
  }
};

const clearSkills = () => {
  selectedSkills.value = [];
};

const setTab = (tabKey) => {
  activeTab.value = tabKey;
  visibleCount.value = jobsPerPage;
};

const resetFilters = () => {
  searchQuery.value = "";
  jobTypeFilter.value = "";
  experienceFilter.value = "";
  locationFilter.value = "";
  sortOption.value = "LATEST";
  selectedSkills.value = [];
  activeTab.value = "all";
  visibleCount.value = jobsPerPage;
};

const filteredJobsBase = computed(() => {
  let list = [...jobs.value];

  // TAB FILTER
  if (activeTab.value === "recommended") {
    list = list.filter((job) => strongMatch(job));
  } else if (activeTab.value === "applied") {
    list = list.filter((job) => appliedJobIds.value.has(job.job_id));
  } else if (activeTab.value === "saved") {
    list = list.filter((job) => savedJobIds.value.has(job.job_id));
  }

  // SEARCH
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter((job) => {
      const title = (job.job_title || "").toLowerCase();
      const loc = (job.location || "").toLowerCase();
      const desc = (job.description || "").toLowerCase();
      return (
        title.includes(q) ||
        loc.includes(q) ||
        desc.includes(q)
      );
    });
  }

  // JOB TYPE
  if (jobTypeFilter.value) {
    list = list.filter((job) => (job.job_type || "") === jobTypeFilter.value);
  }

  // EXPERIENCE
  if (experienceFilter.value !== "") {
    const minExp = Number(experienceFilter.value);
    list = list.filter((job) => {
      const exp = Number(job.experience || 0);
      return exp >= minExp;
    });
  }

  // LOCATION QUICK FILTER
  if (locationFilter.value) {
    const loc = locationFilter.value.toLowerCase();
    list = list.filter((job) => (job.location || "").toLowerCase().includes(loc));
  }

  // SKILLS
  if (selectedSkills.value.length) {
    list = list.filter((job) => {
      const jobSkills = deriveJobSkills(job);
      return selectedSkills.value.every((sk) => jobSkills.includes(sk));
    });
  }

  return list;
});

// SORTED
const filteredJobs = computed(() => {
  const list = [...filteredJobsBase.value];

  if (sortOption.value === "LATEST") {
    return list.sort((a, b) => (b.start_date || "").localeCompare(a.start_date || ""));
  }
  if (sortOption.value === "EARLIEST") {
    return list.sort((a, b) => (a.start_date || "").localeCompare(b.start_date || ""));
  }
  if (sortOption.value === "EXP_ASC") {
    return list.sort((a, b) => (Number(a.experience || 0) - Number(b.experience || 0)));
  }
  if (sortOption.value === "EXP_DESC") {
    return list.sort((a, b) => (Number(b.experience || 0) - Number(a.experience || 0)));
  }

  return list;
});

// VISIBLE (LOAD MORE)
const visibleJobs = computed(() => {
  return filteredJobs.value.slice(0, visibleCount.value);
});

const loadMore = () => {
  visibleCount.value = Math.min(
    visibleCount.value + jobsPerPage,
    filteredJobs.value.length
  );
};

// Stats
const recommendedJobs = computed(() =>
  jobs.value.filter((job) => strongMatch(job))
);

const refreshStats = () => {
  const totalCard = statsCards.value.find((c) => c.key === "total");
  const savedCard = statsCards.value.find((c) => c.key === "saved");
  const appliedCard = statsCards.value.find((c) => c.key === "applied");

  if (totalCard) totalCard.value = jobs.value.length;
  if (savedCard) savedCard.value = savedJobIds.value.size;
  if (appliedCard) appliedCard.value = appliedJobIds.value.size;
};

// -------------------------------
// SAVED / APPLIED TRACKING
// -------------------------------
const isSaved = (job) => job && savedJobIds.value.has(job.job_id);
const hasApplied = (job) => job && appliedJobIds.value.has(job.job_id); // kept for tabs/stats, not used in UI now

const toggleSave = async (job) => {
  if (!job) return;

  const token = localStorage.getItem("token");
  if (!token) {
    Swal.fire("Not logged in", "Please login again to save jobs.", "warning");
    return;
  }

  const alreadySaved = savedJobIds.value.has(job.job_id);

  try {
    if (alreadySaved) {
      // UNSAVE (DELETE)
      const res = await fetch(`${API_BASE}/save-job/${job.job_id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || data.success === false) {
        Swal.fire(
          "Error",
          data.message || "Failed to remove from saved jobs.",
          "error"
        );
        return;
      }

      savedJobIds.value.delete(job.job_id);

      Swal.fire({
        toast: true,
        position: "top-end",
        icon: "info",
        title: "Removed from saved jobs",
        showConfirmButton: false,
        timer: 1800,
      });

    } else {
      // SAVE (POST)
      const res = await fetch(`${API_BASE}/save-job`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ job_id: job.job_id }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || data.success === false) {
        Swal.fire(
          "Error",
          data.message || "Failed to save job.",
          "error"
        );
        return;
      }

      savedJobIds.value.add(job.job_id);

      Swal.fire({
        toast: true,
        position: "top-end",
        icon: "success",
        title: "Job saved",
        showConfirmButton: false,
        timer: 1800,
      });
    }

    persistLocalState();
    refreshStats();
  } catch (err) {
    Swal.fire(
      "Error",
      "Server error while updating saved jobs.",
      "error"
    );
  }
};

// -------------------------------
// JOB DETAILS MODAL + APPLY MODAL
// -------------------------------
const jobDetailsModalRef = ref(null);
let jobDetailsModalInstance = null;

const applyModalRef = ref(null);
let applyModalInstance = null;
const jobForApply = ref(null);

const openJobDetails = (job) => {
  selectedJob.value = job;
  if (jobDetailsModalInstance) {
    jobDetailsModalInstance.show();
  }
};

const openApplyComingSoon = (job) => {
  jobForApply.value = job;
  if (applyModalInstance) {
    applyModalInstance.show();
  }
};

// -------------------------------
// LOCAL STORAGE PERSISTENCE
// -------------------------------
const persistLocalState = () => {
  const saveArr = Array.from(savedJobIds.value);
  const appliedArr = Array.from(appliedJobIds.value);
  localStorage.setItem("candidate_saved_jobs", JSON.stringify(saveArr));
  localStorage.setItem("candidate_applied_jobs", JSON.stringify(appliedArr));
};

const restoreLocalState = () => {
  const savedRaw = localStorage.getItem("candidate_saved_jobs");
  const appliedRaw = localStorage.getItem("candidate_applied_jobs");
  if (savedRaw) {
    try {
      const arr = JSON.parse(savedRaw);
      savedJobIds.value = new Set(arr);
    } catch {}
  }
  if (appliedRaw) {
    try {
      const arr = JSON.parse(appliedRaw);
      appliedJobIds.value = new Set(arr);
    } catch {}
  }
};

// -------------------------------
// BACKEND: SAVED JOB IDS
// -------------------------------
const fetchSavedJobs = async () => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/saved-jobs`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok && data.success) {
      const ids = data.saved_job_ids || [];
      savedJobIds.value = new Set(ids);
      persistLocalState();
      refreshStats();
    }
  } catch (err) {
    // Silent fail – just keep local state
    console.error("Failed to fetch saved jobs", err);
  }
};

// -------------------------------
// LOAD JOBS FROM BACKEND
// -------------------------------
const loadJobs = async () => {
  loading.value = true;
  try {
    // Use /api/jobs-all from backend
    const res = await fetch(`${API_BASE}/jobs-all`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    const data = await res.json();
    if (!res.ok || data.success === false) {
      Swal.fire(
        "Error",
        data.message || data.error || "Failed to load jobs for candidate.",
        "error"
      );
      jobs.value = [];
    } else {
      jobs.value = data.jobs || [];
    }
  } catch (err) {
    Swal.fire("Error", "Server error while fetching jobs.", "error");
    jobs.value = [];
  } finally {
    loading.value = false;
    refreshStats();
  }
};

// -------------------------------
// MOUNT
// -------------------------------
onMounted(() => {
  restoreLocalState();
  loadJobs();
  fetchSavedJobs();

  if (jobDetailsModalRef.value) {
    jobDetailsModalInstance = new Modal(jobDetailsModalRef.value);
  }
  if (applyModalRef.value) {
    applyModalInstance = new Modal(applyModalRef.value);
  }

  window.addEventListener("saved-jobs-updated", () => {
  restoreLocalState();
  refreshStats();
  });
});
</script>

<style scoped>
.candidate-dashboard-page {
  min-height: 100vh;
  background: radial-gradient(circle at top left, #e0edff, #eef4ff 40%, #e7f1ff 70%, #dde8ff);
}

.candidate-dashboard-section {
  min-height: calc(100vh - 70px);
}

/* Fade-in */
.fade-in.visible {
  animation: fadeInUp 0.6s ease forwards;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(14px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

/* Stats cards */
.stats-card {
  border-radius: 1.1rem;
  background: linear-gradient(135deg, #ffffff, #edf2ff);
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.12);
  border: 1px solid rgba(148, 163, 184, 0.2);
  transition: 0.2s ease;
  min-height: 110px;
  display: flex;
  width: 100%;
}
.stats-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 30px rgba(15, 23, 42, 0.18);
}
.stats-icon {
  width: 38px;
  height: 38px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 20% 20%, #0d6efd, #2563eb);
  color: #fff;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.stats-label {
  line-height: 1.1;
}
.stats-value {
  line-height: 1.1;
}

/* Filter card */
.filter-card {
  border-radius: 1.5rem;
}

/* Search box */
.search-box .form-control {
  box-shadow: none;
}
.search-box .form-control::placeholder {
  font-size: 0.85rem;
}

/* Skill chips */
.skill-chip {
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  background: rgba(255, 255, 255, 0.9);
  font-size: 0.8rem;
  padding: 4px 12px;
}
.skill-chip-active {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  color: #fff;
  border-color: transparent;
}

/* Tabs */
.tab-pills .nav-link {
  border-radius: 999px;
  font-size: 0.85rem;
  padding-inline: 16px;
  padding-block: 6px;
  color: #0d6efd;
  background: transparent;
}
.tab-pills .nav-link.active {
  background: #0d6efd;
  color: #fff;
}
.tab-count {
  background: rgba(255, 255, 255, 0.15);
  font-size: 0.7rem;
}

/* Job card */
.job-card {
  border-radius: 1.4rem;
  transition: transform 0.25s ease, box-shadow 0.25s ease, translate 0.25s ease;
}
.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.22);
}

.job-snippet {
  line-height: 1.4;
}

/* Favorite (save) button */
.favorite-btn {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.55);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  font-size: 1.1rem;
  transition: 0.2s ease;
}
.favorite-btn:hover {
  transform: translateY(-1px) scale(1.03);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.18);
}
.favorite-btn-active {
  border-color: transparent;
  background: #e0f2fe;
  color: #0ea5e9;
}

/* Small pill badge */
.small-pill {
  font-size: 0.75rem;
  padding-inline: 10px;
  padding-block: 4px;
}

/* Skeletons */
.job-card-skeleton {
  border-radius: 1.4rem;
  position: relative;
  overflow: hidden;
}
.skeleton-line {
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    #edf2ff 0%,
    #e2e8f0 50%,
    #edf2ff 100%
  );
  animation: shimmer 1.3s infinite linear;
}
.skeleton-pill-group {
  display: flex;
  gap: 6px;
}
.skeleton-pill {
  width: 60px;
  height: 18px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    #edf2ff 0%,
    #e2e8f0 50%,
    #edf2ff 100%
  );
  animation: shimmer 1.3s infinite linear;
}
@keyframes shimmer {
  0% {
    transform: translateX(-10%);
  }
  100% {
    transform: translateX(10%);
  }
}

/* Glass modal */
.glass-modal {
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(18px);
  border-radius: 1.4rem;
}

/* Markdown body in modal */
.markdown-body {
  line-height: 1.5;
}
.markdown-body h3,
.markdown-body h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0.75rem;
}
.markdown-body ul {
  padding-left: 1.2rem;
  margin-bottom: 0.5rem;
}
.markdown-body li {
  margin-bottom: 0.15rem;
}
</style>
