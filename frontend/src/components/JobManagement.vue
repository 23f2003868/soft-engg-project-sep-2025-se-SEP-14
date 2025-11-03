<template>
  <section class="job-management-section py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5 fade-in visible">
        <h2 class="fw-bold text-primary">Job Management</h2>
        <p class="text-muted">Manage all your posted jobs in one place.</p>
      </div>

      <!-- Add New Job Button -->
      <div class="text-end mb-4 fade-in visible">
        <button class="btn btn-primary rounded-3 shadow-sm" @click="openAddJobModal">
          <i class="bi bi-plus-circle me-2"></i> Add New Job
        </button>
      </div>

      <!-- Job List -->
      <div v-if="jobs.length" class="row g-4">
        <div
          v-for="(job, index) in jobs"
          :key="index"
          class="col-md-6 col-lg-4 fade-in visible"
        >
          <div class="job-card bg-white rounded-4 shadow-sm p-4 h-100">
            <h5 class="fw-bold text-dark">{{ job.title }}</h5>
            <p class="text-muted mb-1">
              <i class="bi bi-geo-alt me-1 text-primary"></i> {{ job.location }}
            </p>
            <p class="text-muted mb-2">
              <i class="bi bi-briefcase me-1 text-primary"></i> {{ job.type }}
            </p>
            <p class="small text-secondary mb-3">{{ job.description }}</p>

            <div class="d-flex justify-content-between flex-wrap gap-2">
              <button class="btn btn-outline-primary btn-sm rounded-3" @click="editJob(index)">
                <i class="bi bi-pencil-square"></i> Edit
              </button>
              <button class="btn btn-outline-info btn-sm rounded-3" @click="viewApplicants(job)">
                <i class="bi bi-people"></i> View Applicants
              </button>
              <button class="btn btn-outline-danger btn-sm rounded-3" @click="deleteJob(index)">
                <i class="bi bi-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center text-muted fade-in visible mt-5">
        <i class="bi bi-briefcase fs-1 text-secondary d-block mb-2"></i>
        <p>No jobs posted yet. Start by adding your first job!</p>
      </div>
    </div>

    <!-- Add/Edit Job Modal -->
    <div class="modal fade" id="jobModal" tabindex="-1" ref="jobModalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 border-0 shadow">
          <div class="modal-header">
            <h5 class="modal-title fw-bold">
              {{ editIndex !== null ? 'Edit Job' : 'Add New Job' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveJob">
              <div class="mb-3">
                <label class="form-label">Job Title</label>
                <input
                  v-model="form.title"
                  type="text"
                  class="form-control"
                  placeholder="Enter job title"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Location</label>
                <input
                  v-model="form.location"
                  type="text"
                  class="form-control"
                  placeholder="Enter location"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Job Type</label>
                <select v-model="form.type" class="form-select" required>
                  <option value="">Select Type</option>
                  <option>Full-time</option>
                  <option>Part-time</option>
                  <option>Internship</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  rows="3"
                  placeholder="Enter job description"
                ></textarea>
              </div>
              <div class="text-end">
                <button type="submit" class="btn btn-primary rounded-3">
                  {{ editIndex !== null ? 'Update Job' : 'Add Job' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- View Applicants Modal -->
    <div class="modal fade" id="applicantsModal" tabindex="-1" ref="applicantsModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content rounded-4 border-0 shadow">
          <div class="modal-header bg-light d-flex justify-content-between align-items-center">
            <h5 class="modal-title fw-bold text-primary">
              Applicants for {{ selectedJob?.title }}
            </h5>
            <div class="d-flex align-items-center gap-2">
              <button class="btn btn-outline-success btn-sm" @click="downloadCSV">
                <i class="bi bi-download"></i> Export CSV
              </button>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
          </div>

          <div class="modal-body">
            <!-- Search Filter -->
            <div class="input-group mb-3">
              <span class="input-group-text bg-primary text-white">
                <i class="bi bi-search"></i>
              </span>
              <input
                type="text"
                class="form-control"
                placeholder="Search by name, qualification, or filter by score..."
                v-model="searchQuery"
              />
            </div>

            <!-- Score Filter -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Minimum Score:</label>
              <input
                type="range"
                min="0"
                max="100"
                v-model.number="minScore"
                class="form-range"
              />
              <small class="text-muted">Showing applicants with score ≥ {{ minScore }}</small>
            </div>

            <!-- Applicants Table -->
            <div v-if="filteredApplicants.length">
              <table class="table table-striped align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Qualification</th>
                    <th>Resume</th>
                    <th>Test Score</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(applicant, i) in filteredApplicants" :key="i">
                    <td>{{ applicant.name }}</td>
                    <td>{{ applicant.email }}</td>
                    <td>{{ applicant.qualification }}</td>
                    <td>
                      <a
                        :href="applicant.resume"
                        target="_blank"
                        class="btn btn-outline-secondary btn-sm"
                      >
                        <i class="bi bi-file-earmark-pdf"></i> View
                      </a>
                    </td>
                    <td><span class="badge bg-success">{{ applicant.score }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="text-center text-muted">
              <i class="bi bi-person-x fs-1 text-secondary d-block mb-2"></i>
              <p>No applicants found.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";

const jobs = ref([
  { title: "Frontend Developer", location: "Bangalore", type: "Full-time", description: "Vue.js + Bootstrap developer" },
  { title: "Backend Engineer", location: "Remote", type: "Internship", description: "Work with Flask APIs" },
]);

const applicants = ref({
  "Frontend Developer": [
    { name: "Ananya Gupta", email: "ananya@example.com", qualification: "B.Tech CSE", resume: "assets/resume-ananya.pdf", score: 89 },
    { name: "Rahul Sharma", email: "rahul@example.com", qualification: "MCA", resume: "assets/resume-rahul.pdf", score: 92 },
    { name: "Kiran Mehta", email: "kiran@example.com", qualification: "B.Sc CS", resume: "assets/resume-kiran.pdf", score: 75 },
  ],
  "Backend Engineer": [
    { name: "Pooja Patel", email: "pooja@example.com", qualification: "B.Tech IT", resume: "assets/resume-pooja.pdf", score: 85 },
    { name: "Ravi Kumar", email: "ravi@example.com", qualification: "M.Tech CSE", resume: "assets/resume-ravi.pdf", score: 95 },
  ],
});

const form = ref({ title: "", location: "", type: "", description: "" });
const editIndex = ref(null);
const jobModalRef = ref(null);
const applicantsModalRef = ref(null);
const selectedJob = ref(null);
const searchQuery = ref("");
const minScore = ref(0);

let jobModalInstance = null;
let applicantsModalInstance = null;

const sortedApplicants = computed(() => {
  if (!selectedJob.value) return [];
  const list = applicants.value[selectedJob.value.title] || [];
  return [...list].sort((a, b) => b.score - a.score);
});

const filteredApplicants = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return sortedApplicants.value.filter(
    (a) =>
      (a.name.toLowerCase().includes(query) ||
        a.qualification.toLowerCase().includes(query)) &&
      a.score >= minScore.value
  );
});

const openAddJobModal = () => {
  form.value = { title: "", location: "", type: "", description: "" };
  editIndex.value = null;
  jobModalInstance.show();
};

const editJob = (index) => {
  form.value = { ...jobs.value[index] };
  editIndex.value = index;
  jobModalInstance.show();
};

const deleteJob = (index) => {
  Swal.fire({
    title: "Delete Job?",
    text: "Are you sure you want to delete this job?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.isConfirmed) {
      jobs.value.splice(index, 1);
      Swal.fire("Deleted!", "Job deleted successfully.", "success");
    }
  });
};

const viewApplicants = (job) => {
  selectedJob.value = job;
  searchQuery.value = "";
  minScore.value = 0;
  applicantsModalInstance.show();
};

const saveJob = () => {
  if (!form.value.title || !form.value.location || !form.value.type) {
    Swal.fire("Error", "Please fill all required fields.", "error");
    return;
  }

  if (editIndex.value !== null) {
    jobs.value[editIndex.value] = { ...form.value };
    Swal.fire("Updated!", "Job updated successfully.", "success");
  } else {
    jobs.value.push({ ...form.value });
    Swal.fire("Added!", "New job added successfully.", "success");
  }
  jobModalInstance.hide();
};

const downloadCSV = () => {
  if (!filteredApplicants.value.length) {
    Swal.fire("No data!", "No applicants to export.", "info");
    return;
  }

  const header = ["Name", "Email", "Qualification", "Resume", "Score"];
  const rows = filteredApplicants.value.map(a => [a.name, a.email, a.qualification, a.resume, a.score]);
  const csvContent = [header, ...rows].map(e => e.join(",")).join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `${selectedJob.value.title}-Applicants.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

onMounted(() => {
  jobModalInstance = new Modal(jobModalRef.value);
  applicantsModalInstance = new Modal(applicantsModalRef.value);
});
</script>
