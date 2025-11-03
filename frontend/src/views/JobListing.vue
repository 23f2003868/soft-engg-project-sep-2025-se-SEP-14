<template>
  <Navbar />

  <section class="job-listing-section py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5 fade-in">
        <h2 class="fw-bold text-primary mb-2">Available Job Listings</h2>
        <p class="text-muted fs-5">
          Find your next opportunity from top companies hiring today.
        </p>
      </div>

      <!-- Search and Filter -->
      <div class="row mb-4 fade-in">
        <div class="col-md-8 mx-auto">
          <div class="d-flex flex-column flex-md-row gap-3">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control rounded-4 shadow-sm"
              placeholder="Search job title or company..."
            />
            <select v-model="selectedCategory" class="form-select rounded-4 shadow-sm">
              <option value="">All Categories</option>
              <option>Software Development</option>
              <option>Marketing</option>
              <option>Design</option>
              <option>Finance</option>
              <option>Human Resources</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Job Cards -->
      <div class="row g-4">
        <div
          v-for="(job, index) in filteredJobs"
          :key="index"
          class="col-md-6 col-lg-4 fade-in"
        >
          <div class="job-card bg-white p-4 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex align-items-center mb-3">
                <img
                  :src="job.logo"
                  alt="Company Logo"
                  class="me-3 rounded-circle border"
                  width="55"
                  height="55"
                />
                <div>
                  <h5 class="fw-bold mb-0">{{ job.title }}</h5>
                  <small class="text-muted">{{ job.company }}</small>
                </div>
              </div>
              <p class="text-secondary mb-3">{{ job.description }}</p>
            </div>
            <div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge bg-primary bg-opacity-10 text-primary px-3 py-2">
                  {{ job.category }}
                </span>
                <small class="text-muted">
                  <i class="bi bi-geo-alt me-1"></i>{{ job.location }}
                </small>
              </div>
              <button class="btn btn-primary w-100 mt-3 rounded-4">
                Apply Now
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-if="filteredJobs.length === 0" class="text-center mt-5 fade-in">
        <i class="bi bi-search fs-1 text-secondary"></i>
        <p class="mt-3 text-muted">No matching jobs found.</p>
      </div>
    </div>
  </section>
</template>

<script setup>

import Navbar from '../components/Navbar.vue';
import { ref, computed, onMounted } from "vue";

const searchQuery = ref("");
const selectedCategory = ref("");

const jobs = ref([
  {
    title: "Frontend Developer",
    company: "TechNova Solutions",
    location: "Bangalore",
    category: "Software Development",
    description: "Build modern, responsive UIs using Vue.js and REST APIs.",
    logo: "https://cdn-icons-png.flaticon.com/512/5968/5968705.png",
  },
  {
    title: "Digital Marketing Executive",
    company: "MarketX Media",
    location: "Mumbai",
    category: "Marketing",
    description: "Plan and execute online marketing campaigns for brands.",
    logo: "https://cdn-icons-png.flaticon.com/512/5968/5968520.png",
  },
  {
    title: "UI/UX Designer",
    company: "Designify",
    location: "Remote",
    category: "Design",
    description: "Create intuitive and engaging user experiences and visuals.",
    logo: "https://cdn-icons-png.flaticon.com/512/5968/5968709.png",
  },
  {
    title: "Finance Analyst",
    company: "GrowCorp",
    location: "Delhi",
    category: "Finance",
    description: "Analyze market trends and financial data to guide decisions.",
    logo: "https://cdn-icons-png.flaticon.com/512/2331/2331941.png",
  },
  {
    title: "HR Manager",
    company: "PeopleFirst HR",
    location: "Pune",
    category: "Human Resources",
    description: "Oversee recruitment and employee engagement processes.",
    logo: "https://cdn-icons-png.flaticon.com/512/2331/2331959.png",
  },
]);

const filteredJobs = computed(() => {
  return jobs.value.filter((job) => {
    const matchesSearch =
      job.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      job.company.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCategory =
      !selectedCategory.value || job.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

// Scroll animation setup
onMounted(() => {
  const fadeEls = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );
  fadeEls.forEach((el) => observer.observe(el));
});
</script>

<style scoped>
.job-listing-section {
  background-color: #f8f9fa;
}

/* Fade Animation */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Job Card Styling */
.job-card {
  transition: all 0.3s ease-in-out;
}
.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

button.btn {
  transition: background 0.3s;
}
button.btn:hover {
  background-color: #0a58ca;
}

/* Responsive */
@media (max-width: 768px) {
  .job-listing-section p {
    font-size: 0.95rem;
  }
}
</style>
