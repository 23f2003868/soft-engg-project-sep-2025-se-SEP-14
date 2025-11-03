<template>

  <Navbar />

  <section class="about-section py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5 fade-in">
        <h2 class="fw-bold text-primary mb-2">About Us</h2>
        <p class="text-muted fs-5">
          Empowering connections between <strong>HRs</strong> and <strong>Job Seekers</strong> through innovation and trust.
        </p>
      </div>

      <!-- Mission / Vision Cards -->
      <div class="row g-4">
        <div class="col-md-4 fade-in">
          <div class="about-card h-100 text-center p-4 rounded-4 shadow-sm">
            <div class="icon-circle mx-auto mb-3">
              <i class="bi bi-lightbulb fs-2 text-primary"></i>
            </div>
            <h5 class="fw-bold mb-2">Our Mission</h5>
            <p class="text-secondary">
              To simplify the hiring process and help companies and candidates find the right match with ease and transparency.
            </p>
          </div>
        </div>

        <div class="col-md-4 fade-in">
          <div class="about-card h-100 text-center p-4 rounded-4 shadow-sm">
            <div class="icon-circle mx-auto mb-3">
              <i class="bi bi-rocket-takeoff fs-2 text-primary"></i>
            </div>
            <h5 class="fw-bold mb-2">Our Vision</h5>
            <p class="text-secondary">
              To become the most trusted digital bridge between employers and job seekers, fostering growth and opportunity for all.
            </p>
          </div>
        </div>

        <div class="col-md-4 fade-in">
          <div class="about-card h-100 text-center p-4 rounded-4 shadow-sm">
            <div class="icon-circle mx-auto mb-3">
              <i class="bi bi-people fs-2 text-primary"></i>
            </div>
            <h5 class="fw-bold mb-2">Our Values</h5>
            <p class="text-secondary">
              Integrity, transparency, and innovation drive every connection we help create between HR professionals and candidates.
            </p>
          </div>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="mt-5 text-center fade-in">
        <h4 class="fw-bold text-dark">Why Choose Us?</h4>
        <p class="text-muted mx-auto" style="max-width: 700px;">
          We combine technology with empathy to ensure every user — whether an HR manager or a candidate — experiences
          simplicity, reliability, and success. Our platform is built to evolve with your career and business needs.
        </p>
      </div>

      <!-- Team Section -->
      <div class="team-section mt-5">
        <div class="text-center mb-4 fade-in">
          <h3 class="fw-bold text-primary">Meet Our Team</h3>
          <p class="text-muted">The people behind ApplAI's innovation and success</p>
        </div>

        <div class="row g-4 justify-content-center">
          <div
            class="col-md-3 col-sm-6 fade-in"
            v-for="member in teamMembers"
            :key="member.name"
          >
            <div class="team-card text-center p-4 rounded-4 shadow-sm h-100">
              <img
                :src="member.photo"
                :alt="member.name"
                class="team-photo mb-3"
              />
              <h5 class="fw-bold text-dark mb-1">{{ member.name }}</h5>
              <p class="text-primary fw-semibold mb-1">{{ member.role }}</p>
              <p class="text-muted small">{{ member.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Navbar from '../components/Navbar.vue';

const teamMembers = ref([
  {
    name: "Prasoon",
    role: "Product Manager",
    photo: "/images/team/Prasoon.jpg",
    desc: "Leads product vision and ensures alignment with business goals."
  },
  {
    name: "Deval",
    role: "Architect / Git Version Control Manager",
    photo: "/images/team/Deval.jpg",
    desc: "Manages code structure, branching strategy, and system design."
  },
  {
    name: "Shyaam",
    role: "Scrum Master",
    photo: "/images/team/Shyaam.jpg",
    desc: "Facilitates agile practices and ensures smooth sprint execution."
  },
  {
    name: "Tripurari Kumar",
    role: "Frontend Developer",
    photo: "/images/team/Tripurari.jpg",
    desc: "Builds engaging user interfaces with modern frontend technologies."
  },
  {
    name: "Anushka",
    role: "Frontend Developer",
    photo: "/images/team/Anushka.jpg",
    desc: "Focuses on responsive design and UI enhancements."
  },
  {
    name: "Mangesh",
    role: "Backend Developer",
    photo: "/images/team/Mangesh.jpg",
    desc: "Develops APIs, manages databases, and ensures server-side performance."
  },
  {
    name: "Praul",
    role: "Backend Developer",
    photo: "/images/team/Praul.jpg",
    desc: "Optimizes backend workflows and contributes to scalable architectures."
  },
  {
    name: "Suvrat",
    role: "Tester",
    photo: "/images/team/Suvrat.jpg",
    desc: "Ensures quality assurance through thorough testing and validation."
  }
]);

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
.about-section {
  background-color: #f8f9fa;
}

/* Fade-in Animation */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

.about-card {
  transition: all 0.3s ease-in-out;
  background-color: #fff;
}

.about-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.icon-circle {
  width: 70px;
  height: 70px;
  background-color: #eaf3ff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

/* Team Section */
.team-section {
  margin-top: 4rem;
}

.team-card {
  background-color: #fff;
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 114, 255, 0.2);
}

.team-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #0072ff;
}

@media (max-width: 768px) {
  .about-section p {
    font-size: 0.95rem;
  }
}
</style>
