<template>
  <div class="job-card glass-card p-4 d-flex flex-column h-100">

    <!-- TITLE + COMPANY + LOCATION -->
    <div class="d-flex justify-content-between align-items-start mb-3">

      <!-- Avatar -->
      <div class="job-avatar">
        <img :src="generateJobAvatar(job.job_title)" />
      </div>

      <div class="flex-grow-1 ms-3">

        <!-- Title -->
        <h5 class="fw-bold text-dark mb-1">{{ job.job_title }}</h5>

        <!-- Company -->
        <div class="small text-primary fw-semibold mb-1">
          <i class="bi bi-building me-1"></i>
          {{ job.company || "Unknown Company" }}
        </div>

        <!-- Location -->
        <div class="small text-muted">
          <i class="bi bi-geo-alt me-1 text-primary"></i>{{ job.location }}
        </div>
      </div>

      <!-- Strong Match Tag (Optional) -->
      <span
        v-if="strongMatch"
        class="badge rounded-pill bg-success-subtle text-success fw-semibold small-pill"
      >
        Strong match
      </span>
    </div>

    <!-- META -->
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

    <!-- DESCRIPTION -->
    <p class="job-snippet text-secondary small mt-2 mb-3">
      {{ shortDesc }}
    </p>

    <!-- SKILLS -->
    <div class="mb-3 d-flex flex-wrap gap-1">
      <span
        v-for="skill in skills"
        :key="skill"
        class="badge rounded-pill bg-light text-primary border small-pill"
      >
        {{ skill }}
      </span>
    </div>

    <!-- ACTIONS -->
    <div class="d-flex justify-content-between align-items-center mt-auto">
      <button
        class="btn btn-sm btn-outline-primary rounded-pill"
        @click="$emit('view', job)"
      >
        View Details
      </button>

      <div class="d-flex gap-2">

        <!-- SAVE -->
        <button
          class="btn btn-sm rounded-circle favorite-btn"
          :class="{ 'favorite-btn-active': saved }"
          @click="$emit('save', job)"
        >
          <i :class="saved ? 'bi bi-bookmark-fill' : 'bi bi-bookmark'"></i>
        </button>

        <!-- APPLY -->
        <button
          class="btn btn-sm btn-success rounded-pill"
          :disabled="applied || testDone"
          @click="$emit('apply', job)"
        >
          {{ applied ? "Applied" : testDone ? "Test Done" : "Apply" }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  job: Object,
  saved: Boolean,
  applied: Boolean,
  testDone: Boolean,
  strongMatch: Boolean,
  skills: Array,
});

const emit = defineEmits(["view", "save", "apply"]);

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

function shortDesc(desc) {
  if (!desc) return "No description.";
  const clean = desc.replace(/[#*_`]/g, " ").replace(/\s+/g, " ").trim();
  return clean.length <= 140 ? clean : clean.slice(0, 140) + "...";
}

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
  return d.toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}
</script>

<style scoped>
/* exact same as candidate dashboard */
.job-card {
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(220, 227, 240, 0.65);
  backdrop-filter: blur(14px);
  transition: 0.28s ease;
}

.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 22px 46px rgba(25, 40, 70, 0.22);
}

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

.favorite-btn {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.55);
  background: #fff;
}

.favorite-btn-active {
  background: #e0f2fe;
  border-color: transparent;
  color: #0284c7;
}
</style>
