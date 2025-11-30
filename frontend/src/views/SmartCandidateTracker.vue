<template>
    <Topbar />
  <div class="kanban-wrapper bg-light min-vh-100 py-5 px-3">
    <!-- Header -->
    <div class="text-center mb-5">
      <h2 class="fw-bold text-primary">Smart Candidate Tracker</h2>
      <p class="text-muted">Drag and drop candidates between stages</p>
    </div>

    <!-- Search -->
    <div class="d-flex justify-content-center mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search candidate or job title..."
        class="form-control w-75 w-md-50 shadow-sm rounded-pill px-4 py-2"
      />
    </div>

    <!-- Kanban Columns -->
    <div class="row g-4 justify-content-center">
      <div
        v-for="(stage, index) in stages"
        :key="stage.name"
        class="col-12 col-md-6 col-lg-2 d-flex flex-column"
      >
        <div class="card border-0 shadow-sm flex-grow-1">
          <div
            class="card-header fw-bold text-center text-white"
            :style="{ backgroundColor: stage.color }"
          >
            {{ stage.name }}
          </div>

          <div class="card-body p-3 overflow-auto" style="max-height: 65vh;">
            <!-- Draggable Container -->
            <draggable
              v-model="stage.candidates"
              :group="'candidates'"
              class="list-group"
              item-key="id"
              @end="onDragEnd"
            >
              <template #item="{ element }">
                <div
                  v-if="isVisible(element)"
                  class="candidate-card border rounded-3 p-3 mb-3 bg-white shadow-sm"
                >
                  <h6 class="fw-semibold text-dark mb-1">
                    <i class="bi bi-person-circle me-2 text-primary"></i>
                    {{ element.name }}
                  </h6>
                  <p class="text-muted small mb-1">
                    <i class="bi bi-briefcase me-1"></i>{{ element.jobTitle }}
                  </p>
                  <p class="text-muted small mb-0">
                    <i class="bi bi-envelope me-1"></i>{{ element.email }}
                  </p>
                </div>
              </template>
            </draggable>

            <!-- Empty message -->
            <p
              v-if="stage.candidates.filter(isVisible).length === 0"
              class="text-muted small text-center mt-3"
            >
              No candidates
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import draggable from "vuedraggable";
import Topbar from "../components/RecruiterNavbar.vue";

const searchQuery = ref("");

const stages = ref([
  {
    name: "Applied",
    color: "#9BBDF9",
    candidates: [
      { id: 1, name: "Aarav Mehta", email: "aarav.mehta@example.com", jobTitle: "Frontend Developer" },
      { id: 6, name: "Kritika Das", email: "kritika.das@example.com", jobTitle: "UI Designer" },
    ],
  },
  {
    name: "Shortlisted",
    color: "#7EC8E3",
    candidates: [
      { id: 2, name: "Neha Sharma", email: "neha.sharma@example.com", jobTitle: "Backend Developer" },
      { id: 7, name: "Rahul Iyer", email: "rahul.iyer@example.com", jobTitle: "Frontend Developer" },
    ],
  },
  {
    name: "Interviewed",
    color: "#FBC252",
    candidates: [
      { id: 3, name: "Rohit Verma", email: "rohit.verma@example.com", jobTitle: "Data Analyst" },
      { id: 8, name: "Sneha Patel", email: "sneha.patel@example.com", jobTitle: "Data Analyst" },
    ],
  },
  {
    name: "Offered",
    color: "#81C784",
    candidates: [
      { id: 4, name: "Ananya Gupta", email: "ananya.gupta@example.com", jobTitle: "ML Engineer" },
    ],
  },
  {
    name: "Hired",
    color: "#4CAF50",
    candidates: [
      { id: 5, name: "Vikram Singh", email: "vikram.singh@example.com", jobTitle: "Full Stack Developer" },
    ],
  },
]);

const isVisible = (candidate) => {
  return (
    candidate.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    candidate.jobTitle.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
};

const onDragEnd = (event) => {
  console.log("Moved candidate:", event.item.__draggable_context.element.name);
  console.log("From:", event.from.dataset.stage, "To:", event.to.dataset.stage);
};
</script>

<style scoped>
.kanban-wrapper {
  background: linear-gradient(180deg, #f9fafc 0%, #eef3f8 100%);
}

.card {
  border-radius: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  border-top-left-radius: 16px !important;
  border-top-right-radius: 16px !important;
  font-size: 1rem;
  letter-spacing: 0.5px;
}

.candidate-card {
  transition: all 0.2s ease-in-out;
  cursor: grab;
}

.candidate-card:hover {
  background-color: #f8faff;
  transform: scale(1.02);
  border-color: #b3d4fc;
}

@media (max-width: 768px) {
  .card-body {
    max-height: none;
  }
  .card {
    margin-bottom: 1rem;
  }
}
</style>
