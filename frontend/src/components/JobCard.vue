<template>
  <div class="job-card glass-card p-4 h-100 d-flex flex-column">

    <!-- HEADER -->
    <div class="d-flex justify-content-between align-items-start mb-2">
      <div>
        <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>

        <div class="small text-muted">
          <i class="bi bi-geo-alt me-1 text-primary"></i>
          {{ job.location || "Location not specified" }}
        </div>
      </div>

      <span
        v-if="strongMatch"
        class="badge rounded-pill bg-success-subtle text-success fw-semibold small-pill"
      >
        Strong match
      </span>
    </div>

    <!-- JOB META -->
    <div class="small text-muted mb-1">
      <span class="me-2">
        <i class="bi bi-briefcase me-1 text-primary"></i>
        {{ job.job_type }}
      </span>

      <span>
        <i class="bi bi-clock-history me-1 text-primary"></i>
        Posted {{ relativeDate(job.start_date) }}
      </span>
    </div>

    <div class="small text-muted mb-1">
      <i class="bi bi-person-workspace me-1 text-primary"></i>
      Experience:
      <span class="fw-semibold">{{ formatExperience(job.experience) }}</span>
    </div>

    <div class="small text-muted mb-2">
      <i class="bi bi-calendar-event me-1 text-primary"></i>
      End Date:
      <span class="fw-semibold">{{ formatReadableDate(job.end_date) }}</span>
    </div>

    <!-- DESCRIPTION -->
    <p class="job-snippet text-secondary small flex-grow-1">
      {{ shortDescription }}
    </p>

    <!-- SKILLS -->
    <div class="mb-3 d-flex flex-wrap gap-1">
      <span
        v-for="skill in derivedSkills"
        :key="skill"
        class="badge rounded-pill bg-light text-primary border small-pill"
      >
        {{ skill }}
      </span>
    </div>

    <!-- ACTIONS -->
    <div class="d-flex justify-content-between align-items-center mt-2">
      <button
        class="btn btn-sm btn-outline-primary rounded-pill"
        @click="$emit('view-details', job)"
      >
        View Details
      </button>

      <div class="d-flex align-items-center gap-2">

        <!-- SAVE UNSAVE -->
        <button
          class="btn btn-sm rounded-circle favorite-btn"
          :class="{ 'favorite-btn-active': isSaved }"
          @click="$emit('toggle-save', job)"
        >
          <i :class="isSaved ? 'bi bi-bookmark-fill' : 'bi bi-bookmark'"></i>
        </button>

        <!-- APPLY / TEST DONE / APPLIED -->
        <button
          class="btn btn-sm btn-success rounded-pill"
          :disabled="isApplied || testDone"
          @click="$emit('apply', job)"
        >
          {{ isApplied ? "Applied" : testDone ? "Test Done" : "Apply" }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps({
  job: { type: Object, required: true },
  isSaved: { type: Boolean, default: false },
  isApplied: { type: Boolean, default: false },
  testDone: { type: Boolean, default: false },
  candidateSkills: { type: Array, default: () => [] },
  allSkills: { type: Array, default: () => [] }
});

defineEmits(["toggle-save", "apply", "view-details"]);

// --- Compute Skills from Job Description ---
const derivedSkills = computed(() => {
  const text = (props.job.description || "").toLowerCase();
  const set = new Set();
  props.allSkills.forEach((s) => {
    if (text.includes(s.toLowerCase())) set.add(s);
  });
  return Array.from(set).slice(0, 6);
});

// --- Strong Match Logic ---
const strongMatch = computed(() => {
  const intersection = derivedSkills.value.filter((s) =>
    props.candidateSkills.includes(s)
  );
  return intersection.length >= 2;
});

// --- Format Experience ---
const formatExperience = (exp) => {
  if (!exp && exp !== 0) return "Not specified";
  const n = Number(exp);
  if (n === 0) return "Fresher (0 yrs)";
  if (n === 1) return "1 year";
  return `${n} years`;
};

// --- Relative Date ---
const relativeDate = (raw) => {
  if (!raw) return "date unknown";
  const d = new Date(raw);
  if (isNaN(d)) return "date unknown";

  const diff = (new Date() - d) / (1000 * 60 * 60 * 24);
  if (diff <= 0) return "today";
  if (diff < 1) return "today";
  if (diff < 2) return "1 day ago";
  if (diff < 7) return `${Math.floor(diff)} days ago`;
  const w = Math.floor(diff / 7);
  if (w < 4) return `${w} weeks ago`;
  return `${Math.floor(diff / 30)} months ago`;
};

const formatReadableDate = (raw) => {
  if (!raw) return "Not specified";
  return new Date(raw).toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

const shortDescription = computed(() => {
  let d = props.job.description || "";
  d = d.replace(/[#*_`>-]/g, " ")
    .replace(/\[(.*?)\]\((.*?)\)/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
  return d.length > 140 ? d.slice(0, 140) + "..." : d;
});
</script>

<style scoped>
.job-card {
  border-radius: 1.4rem;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.22);
}
.small-pill {
  font-size: 0.75rem;
  padding: 4px 10px;
}
.job-snippet {
  line-height: 1.4;
}
.favorite-btn {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.55);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}
.favorite-btn-active {
  background: #e0f2fe;
  color: #0ea5e9;
  border-color: transparent;
}
</style>
