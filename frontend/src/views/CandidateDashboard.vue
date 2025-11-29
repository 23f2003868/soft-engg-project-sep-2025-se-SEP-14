<template>
  <CandidateNavbar />
  <div class="container py-4">
    <!-- Header -->
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4">
      <div class="text-secondary">
        Welcome, <span class="fw-semibold text-primary">{{ userProfile.name }}</span>
      </div>
    </div>

    <!-- Search and Filter -->
    <div class="row g-3 mb-4">
      <div class="col-md-8">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control shadow-sm"
          placeholder="Search by job title, company, or location..."
        />
      </div>
      <div class="col-md-4">
        <select v-model="experienceFilter" class="form-select shadow-sm">
          <option value="">All Experience Levels</option>
          <option value="Fresher">Fresher</option>
          <option value="Mid">Mid Level</option>
          <option value="Senior">Senior</option>
        </select>
      </div>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-pills mb-4">
      <li class="nav-item">
        <button class="nav-link" :class="{ active: activeTab === 'all' }" @click="setTab('all')">All Jobs</button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="{ active: activeTab === 'recommended' }" @click="setTab('recommended')">Recommended</button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="{ active: activeTab === 'applied' }" @click="setTab('applied')">Applied</button>
      </li>
    </ul>

    <!-- Job Listings -->
    <div class="row g-4">
      <div v-for="job in filteredJobList" :key="job.id" class="col-md-6 col-lg-4">
        <div class="card border-0 shadow-sm job-card h-100">
          <div class="card-body">
            <h5 class="fw-bold text-dark mb-1">{{ job.title }}</h5>
            <p class="text-primary fw-semibold mb-1">{{ job.company }}</p>
            <p class="text-muted small mb-2">{{ job.location }}</p>
            <p class="text-muted small mb-3">Experience: {{ job.experience }}</p>

            <div class="mb-3">
              <span v-for="skill in job.skills" :key="skill" class="badge bg-light text-primary border me-1">
                {{ skill }}
              </span>
            </div>

            <div class="d-flex justify-content-between align-items-center">
              <button
                class="btn btn-outline-primary btn-sm"
                @click="openJobModal(job)"
                data-bs-toggle="modal"
                data-bs-target="#jobDetailsModal"
              >
                View Details
              </button>

              <button
                v-if="!hasApplied(job)"
                class="btn btn-success btn-sm"
                @click="startCredibilityTest(job)"
              >
                Apply
              </button>

              <span v-else class="text-success small fw-semibold">Applied</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Jobs Found -->
    <div v-if="filteredJobList.length === 0" class="text-center text-muted mt-5">
      <p>No jobs match your criteria.</p>
    </div>

    <!-- Job Details Modal -->
    <div class="modal fade" id="jobDetailsModal" tabindex="-1" aria-labelledby="jobDetailsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content shadow-lg border-0">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-semibold" id="jobDetailsModalLabel">{{ selectedJob?.title }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Company:</strong> {{ selectedJob?.company }}</p>
            <p><strong>Location:</strong> {{ selectedJob?.location }}</p>
            <p><strong>Experience:</strong> {{ selectedJob?.experience }}</p>
            <hr />
            <h6 class="fw-bold text-primary">Job Description</h6>
            <p>{{ selectedJob?.description }}</p>
            <h6 class="fw-bold text-primary">Required Skills</h6>
            <div>
              <span v-for="skill in selectedJob?.skills" :key="skill" class="badge bg-secondary me-1">{{ skill }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Credibility Test Modal -->
    <div v-if="showTestModal" class="test-modal-overlay">
      <div class="test-modal card shadow-lg p-4">
        <div class="test-header d-flex justify-content-between align-items-center mb-3">
          <span class="fw-semibold text-danger">Time Left: {{ timeLeft }}s</span>
        </div>

        <!-- Small camera preview -->
        <div class="camera-wrapper">
          <video id="cameraPreview" autoplay playsinline muted></video>
        </div>

        <div v-for="(q, index) in testQuestions" :key="index" class="mb-3">
          <p class="fw-semibold">{{ index + 1 }}. {{ q.question }}</p>
          <div v-for="option in q.options" :key="option" class="form-check">
            <input
              class="form-check-input"
              type="radio"
              :name="'question-' + index"
              :value="option"
              v-model="q.selected"
            />
            <label class="form-check-label">{{ option }}</label>
          </div>
        </div>

        <div class="text-end mt-3">
          <button class="btn btn-secondary me-2" @click="cancelTest">Cancel</button>
          <button class="btn btn-success" @click="submitTest">Submit Test</button>
        </div>
      </div>
    </div>

    <FloatingChatBot />
  </div>
</template>

<script setup>
import CandidateNavbar from "../components/CandidateNavbar.vue";
import FloatingChatBot from "../components/ChatBot.vue";
</script>

<script>
export default {
  name: "CandidateDashboard",
  data() {
    return {
      activeTab: "all",
      searchQuery: "",
      experienceFilter: "",
      selectedJob: null,
      showTestModal: false,
      currentJobForTest: null,
      cameraStream: null,
      userProfile: {
        name: "Ravi Kumar",
        skills: ["Python", "Data Analysis", "VueJS"],
        qualification: "B.Tech",
        experience: "Mid",
      },
      jobList: [
        { id: 1, title: "Data Analyst", company: "TechCorp", location: "Bangalore", experience: "Mid", skills: ["Python", "SQL"], description: "Analyze data, prepare insights and build dashboards." },
        { id: 2, title: "Frontend Developer", company: "WebX", location: "Chennai", experience: "Fresher", skills: ["HTML", "VueJS", "CSS"], description: "Develop user interfaces and maintain web components." },
        { id: 3, title: "ML Engineer", company: "AIWorks", location: "Pune", experience: "Senior", skills: ["Python", "ML"], description: "Design and deploy machine learning models." },
      ],
      appliedJobs: [],
      testQuestions: [
        { question: "Which language is used for styling web pages?", options: ["HTML", "Python", "CSS", "C++"], answer: "CSS", selected: null },
        { question: "What does API stand for?", options: ["App Programming Interface", "Application Programming Interface", "Applied Program Internet", "None"], answer: "Application Programming Interface", selected: null },
        { question: "Vue.js is a ___?", options: ["Backend Framework", "Database", "Frontend Framework", "Language"], answer: "Frontend Framework", selected: null },
      ],
      timeLeft: 60,
      timerInterval: null,
    };
  },
  computed: {
    filteredJobList() {
      let jobs = this.activeTab === "recommended"
        ? this.jobList.filter((job) => job.skills.some((s) => this.userProfile.skills.includes(s)))
        : this.activeTab === "applied"
        ? this.appliedJobs
        : this.jobList;

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        jobs = jobs.filter(
          (job) =>
            job.title.toLowerCase().includes(q) ||
            job.company.toLowerCase().includes(q) ||
            job.location.toLowerCase().includes(q)
        );
      }
      if (this.experienceFilter) {
        jobs = jobs.filter((job) => job.experience === this.experienceFilter);
      }
      return jobs;
    },
  },
  methods: {
    setTab(tab) {
      this.activeTab = tab;
    },
    openJobModal(job) {
      this.selectedJob = job;
    },
    async startCredibilityTest(job) {
      this.currentJobForTest = job;
      this.showTestModal = true;
      await this.startCamera();
      this.startTimer();
    },
    async startCamera() {
      try {
        this.cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
        document.getElementById("cameraPreview").srcObject = this.cameraStream;
      } catch {
        alert("Camera access denied.");
      }
    },
    stopCamera() {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach((t) => t.stop());
        this.cameraStream = null;
      }
    },
    startTimer() {
      this.timeLeft = 60;
      this.timerInterval = setInterval(() => {
        if (this.timeLeft > 0) this.timeLeft--;
        else this.submitTestAutomatically();
      }, 1000);
    },
    stopTimer() {
      clearInterval(this.timerInterval);
    },
    cancelTest() {
      this.stopTimer();
      this.stopCamera();
      this.showTestModal = false;
    },
    submitTest() {
      const correct = this.testQuestions.filter((q) => q.selected === q.answer).length;
      this.stopTimer();
      this.stopCamera();
      if (correct >= 2) {
        alert("Test Passed! Job Applied Successfully.");
        this.appliedJobs.push(this.currentJobForTest);
      } else {
        alert("Test Failed.");
      }
      this.showTestModal = false;
    },
    submitTestAutomatically() {
      this.stopTimer();
      this.stopCamera();
      alert("Time Over. Test Submitted Automatically.");
      this.showTestModal = false;
    },
    hasApplied(job) {
      return this.appliedJobs.some((j) => j.id === job.id);
    },
  },
};
</script>

<style scoped>
.job-card {
  transition: all 0.3s ease;
  border-radius: 10px;
}
.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}
.nav-pills .nav-link {
  color: #0d6efd;
  border-radius: 20px;
}
.nav-pills .nav-link.active {
  background-color: #0d6efd;
  color: #fff;
}
.test-modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 2000;
  padding: 1rem;
}
.test-modal {
  width: 700px;
  max-width: 95%;
  background: #fff;
  border-radius: 12px;
  overflow-y: auto;
  max-height: 90vh;
  position: relative;
}
.camera-wrapper {
  position: absolute;
  top: 1rem; right: 1rem;
  width: 120px; height: 90px;
  border: 2px solid #007bff;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
}
.camera-wrapper video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
@media (max-width: 576px) {
  .camera-wrapper {
    width: 90px; height: 70px;
  }
}
</style>
