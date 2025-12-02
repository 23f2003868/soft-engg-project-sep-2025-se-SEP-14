<template>
  <div class="modal fade" ref="root" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content glass-modal border-0">

        <!-- HEADER -->
        <div class="modal-header border-0">
          <div>
            <h5 class="modal-title fw-bold">{{ job?.job_title }}</h5>

            <p class="small text-muted mb-0">
              <i class="bi bi-geo-alt me-1 text-primary"></i>
              {{ job?.location || "Not specified" }}

              <span v-if="job?.job_type">
                • <i class="bi bi-briefcase ms-2 me-1 text-primary"></i>
                {{ job?.job_type }}
              </span>
            </p>

            <p class="small text-muted mb-0">
              Experience:
              <span class="fw-semibold">
                {{ formatExperience(job?.experience) }}
              </span>
            </p>

            <p class="small text-muted mb-0">
              End Date:
              <span class="fw-semibold">
                {{ formatReadableDate(job?.end_date) }}
              </span>
            </p>
          </div>

          <button type="button" class="btn-close" data-bs-dismiss="modal" @click="emitClose"></button>
        </div>

        <!-- BODY -->
        <div class="modal-body pt-0">
          <hr class="mt-0 mb-3" />

          <!-- DESCRIPTION -->
          <h6 class="fw-semibold text-primary mb-2">Job Description</h6>

          <div
            class="small text-secondary mb-3 markdown-body"
            v-html="descriptionHtml"
          ></div>

          <!-- SKILLS -->
          <h6 class="fw-semibold text-primary mb-2">Skills Highlight</h6>

          <div class="mb-3 d-flex flex-wrap gap-1">
            <span
              v-for="skill in derivedSkills"
              :key="skill"
              class="badge rounded-pill bg-light text-primary border small-pill"
            >
              {{ skill }}
            </span>
          </div>

          <!-- ACTION BUTTONS -->
          <div class="d-flex justify-content-end gap-2 mt-2">
            <button
              class="btn btn-outline-primary btn-sm rounded-pill"
              @click="$emit('toggle-save', job)"
            >
              <i class="bi bi-bookmark me-1"></i> Save
            </button>

            <button
              class="btn btn-success btn-sm rounded-pill"
              @click="$emit('apply', job)"
            >
              Apply
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { marked } from "marked";

const root = ref(null);
defineExpose({ root });

const props = defineProps({
  job: { type: Object, default: null },
  allSkills: { type: Array, default: () => [] }
});

const emit = defineEmits(["close", "toggle-save", "apply"]);

const emitClose = () => emit("close");

const descriptionHtml = computed(() => {
  if (!props.job?.description) return "<p>No description available.</p>";
  return marked.parse(String(props.job.description));
});

// Extract skills from job description
const derivedSkills = computed(() => {
  if (!props.job) return [];
  const text = (props.job.description || "").toLowerCase();
  
  const list = props.allSkills.filter(s =>
    text.includes(s.toLowerCase())
  );

  return list.length ? list.slice(0, 8) : ["Communication", "Teamwork"];
});

const formatExperience = (exp) => {
  if (exp === null || exp === undefined || exp === "") return "Not specified";
  const n = Number(exp);
  if (isNaN(n)) return "Not specified";
  if (n === 0) return "Fresher (0 yrs)";
  if (n === 1) return "1 year";
  return `${n} years`;
};

const formatReadableDate = (rawDate) => {
  if (!rawDate) return "Not specified";
  const d = new Date(rawDate);
  if (isNaN(d.getTime())) return "Not specified";
  return d.toLocaleDateString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
};
</script>

<style scoped>
.glass-modal {
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(18px);
  border-radius: 1.4rem;
}

.markdown-body {
  line-height: 1.5;
}

.small-pill {
  font-size: 0.75rem;
  padding-inline: 10px;
  padding-block: 4px;
}

.markdown-body h3,
.markdown-body h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0.75rem;
}
</style>
