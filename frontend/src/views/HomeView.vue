<template>
 <Navbar />
  <div class="home-page pb-5">
    <!-- Hero Section -->
    <section
      class="hero-section text-white py-5 position-relative overflow-hidden"
      style="background: linear-gradient(135deg, #1e3c72, #2a5298);"
    >
      <div class="bubbles">
        <div
          v-for="n in 25"
          :key="n"
          class="bubble"
          :style="{
            left: Math.random() * 100 + '%',
            width: Math.random() * 20 + 10 + 'px',
            height: Math.random() * 20 + 10 + 'px',
            animationDuration: Math.random() * 6 + 8 + 's',
            animationDelay: Math.random() * 5 + 's'
          }"
        ></div>
      </div>

      <div class="container py-5 position-relative" style="z-index: 2;">
        <div class="row align-items-center">
          <div class="col-lg-6 text-center text-lg-start mb-4 mb-lg-0">
            <h1 class="display-5 fw-bold mb-3">
              Discover <span class="text-accent">AI-Powered</span> Career Opportunities 🚀
            </h1>
            <p class="lead text-light opacity-75 mb-4">
              Let our intelligent tools connect you to opportunities that align perfectly with your skills and goals.
            </p>
            <router-link
              to="/jobs"
              class="btn btn-hero btn-lg rounded-4 shadow px-5 py-3"
            >
              Get Started
            </router-link>
          </div>

          <div class="col-lg-6 text-center">
            <img
              src="https://plus.unsplash.com/premium_photo-1661632752188-5fbc13fd4697?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8d29tYW4lMjB3b3JraW5nJTIwb24lMjBsYXB0b3B8ZW58MHx8MHx8fDA%3D&fm=jpg&q=60&w=3000"
              alt="Career Woman with Tablet"
              class="img-fluid floating-girl"
              width="420"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5 bg-light border-top border-bottom">
      <div class="container text-center">
        <h2 class="fw-bold mb-4 text-primary">
          Why Choose <span class="text-accent">ApplAI</span>?
        </h2>
        <p class="text-secondary mb-5">
          Explore how our smart features can help you land your dream role faster.
        </p>

        <div class="row g-4">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="col-md-6 col-lg-4"
          >
            <div class="feature-card p-4 shadow-sm rounded-4 h-100 bg-white position-relative">
              <div class="feature-icon mb-3">
                <img
                  :src="feature.icon"
                  :alt="feature.title"
                  class="img-fluid floating-icon"
                  width="60"
                  height="60"
                />
              </div>
              <h5 class="fw-semibold mb-2">{{ feature.title }}</h5>
              <p class="text-secondary small">{{ feature.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section
      class="stats-section text-white text-center py-5 mt-5"
      style="background: linear-gradient(135deg, #2a5298, #1e3c72);"
    >
      <div class="container">
        <h2 class="fw-bold mb-4">Our Impact So Far</h2>
        <div class="row g-4 justify-content-center">
          <div class="col-md-3 col-6" v-for="(stat, i) in stats" :key="i">
            <h2 class="fw-bold display-6 text-info">{{ stat.number }}</h2>
            <p class="text-light small mb-0">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Trusted Companies Section -->
    <section class="company-section py-5 bg-light border-top">
      <div class="container text-center">
        <h2 class="fw-bold text-primary mb-4">Trusted by Top Companies</h2>
        <p class="text-secondary mb-5">
          Our platform is trusted by leading organizations worldwide.
        </p>

        <!-- Enhanced Logo Grid -->
        <div class="trusted-logos d-flex flex-wrap justify-content-center align-items-center gap-5">
          <div v-for="(logo, index) in companyLogos" :key="index" class="logo-card d-flex align-items-center justify-content-center">
            <img :src="logo" alt="Company Logo" class="company-logo" />
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonial Section -->
    <section class="testimonial-section py-5 text-center text-white">
      <div class="container">
        <h2 class="fw-bold mb-4 text-primary">What Our Users Say</h2>
        <p class="lead text-light opacity-75 mb-5">
          Hear from professionals who’ve found their dream jobs with us.
        </p>

       <div class="testimonial-slider">
          <div
            v-for="(feedback, index) in [...testimonials, ...testimonials]"
            :key="index"
            class="testimonial-card bg-white text-dark rounded-4 shadow p-4"
          >
          <p class="mb-3 fst-italic">"{{ feedback.message }}"</p>
          <h6 class="fw-bold text-primary mb-0">{{ feedback.name }}</h6>
          <small class="text-secondary">{{ feedback.role }}</small>
        </div>
      </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";

const features = ref([
  { title: "AI Job Matching", desc: "Receive smart job suggestions powered by advanced AI models.", icon: "https://cdn-icons-png.flaticon.com/512/4712/4712109.png" },
  { title: "Verified Companies", desc: "Connect only with trusted and verified employers from top industries.", icon: "https://cdn-icons-png.flaticon.com/512/3135/3135715.png" },
  { title: "Skill-Based Search", desc: "Quickly find roles that align with your strengths and aspirations.", icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png" },
  { title: "Resume Builder", desc: "Create an impressive resume in just minutes using our built-in tool.", icon: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png" },
  { title: "Real-Time Alerts", desc: "Get instant updates on new job openings and interview calls.", icon: "https://cdn-icons-png.flaticon.com/512/1827/1827340.png" },
  { title: "Recruiter Dashboard", desc: "Post jobs, review applicants, and manage hiring effortlessly.", icon: "https://cdn-icons-png.flaticon.com/512/3135/3135789.png" },
]);

const stats = ref([
  { number: "10K+", label: "Active Jobs" },
  { number: "5K+", label: "Recruiters" },
  { number: "50K+", label: "Users" },
  { number: "98%", label: "Success Rate" },
]);

import Navbar from '../components/Navbar.vue';

const companyLogos = ref([
  "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
  "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/0/06/Amazon_2024.svg",
  "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/a/aa/LinkedIn_2021.svg",
  "https://www.boat-lifestyle.com/cdn/shop/files/boAt_logo_black_24889e30-925c-4185-a028-9fef497a8e44.svg?v=1732879339", 
  "https://upload.wikimedia.org/wikipedia/commons/c/cd/Accenture.svg",
  "https://upload.wikimedia.org/wikipedia/commons/9/95/Infosys_logo.svg",
  "https://upload.wikimedia.org/wikipedia/en/b/b1/Tata_Consultancy_Services.svg",
  "https://upload.wikimedia.org/wikipedia/commons/8/89/Wipro_new_logo.svg",
  "https://upload.wikimedia.org/wikipedia/en/d/d8/Capgemini_logo.svg",
  "https://upload.wikimedia.org/wikipedia/commons/9/90/Adobe_Corporate_wordmark.svg",
]);

const testimonials = ref([
  // Candidate Feedback
  {
    message: "ApplAI helped me land my dream role in less than two weeks! The job recommendations were spot-on.",
    name: "Sweta Priya",
    role: "Data Analyst at Google",
  },
  {
    message: "The AI-powered suggestions actually matched my interests — this made job searching stress-free!",
    name: "Anjali Verma",
    role: "Software Engineer at Microsoft",
  },
  {
    message: "I built my resume using their AI tool and started getting interview calls the same week!",
    name: "Ravi Kumar",
    role: "Backend Developer at Amazon",
  },
  {
    message: "It felt like ApplAI understood exactly what I was looking for. Highly recommended!",
    name: "Sneha Patel",
    role: "UI/UX Designer at Adobe",
  },
  {
    message: "I’ve tried multiple platforms, but none match the accuracy and speed of ApplAI.",
    name: "Karan Singh",
    role: "DevOps Engineer at IBM",
  },

  // HR Feedback
  {
    message: "As a recruiter, this platform made hiring so much faster. The dashboard is clean and easy to use.",
    name: "Rahul Mehta",
    role: "HR Manager at Accenture",
  },
  {
    message: "Finding top candidates has never been this effortless. ApplAI filters save us hours!",
    name: "Neha Gupta",
    role: "Talent Acquisition Lead at Infosys",
  },
  {
    message: "We filled two tech roles in under a week using ApplAI recruiter dashboard. Brilliant system!",
    name: "Amit Shah",
    role: "HR Executive at Wipro",
  },
  {
    message: "Very intuitive interface. Posting jobs and reviewing applications is super fast.",
    name: "Pooja Nair",
    role: "Recruitment Head at TCS",
  },
  {
    message: "We love how AI recommendations match perfectly with our skill requirements.",
    name: "Vikram Joshi",
    role: "HR Lead at Capgemini",
  },
]);

</script>

<style scoped>
:root {
  --accent-color: #00c6ff;
}

/* Hero Section */
.hero-section {
  min-height: 90vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* Bubble Effect */
.bubbles {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 1;
}
.bubble {
  position: absolute;
  bottom: -120px;
  background: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: rise 12s infinite ease-in;
}
.bubble:nth-child(odd) {
  background: rgba(0, 198, 255, 0.5);
  box-shadow: 0 0 8px rgba(0, 198, 255, 0.4);
}
@keyframes rise {
  0% {
    transform: translateY(0);
    opacity: 0.5;
  }
  50% {
    opacity: 0.9;
  }
  100% {
    transform: translateY(-900px);
    opacity: 0;
  }
}

/* Accent */
.text-accent {
  color: var(--accent-color);
}

/* Button */
.btn-hero {
  background: linear-gradient(135deg, #00c6ff, #0077b6);
  color: white;
  font-weight: 600;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 198, 255, 0.35);
}
.btn-hero:hover {
  background: linear-gradient(135deg, #0096c7, #48cae4);
  transform: scale(1.05) translateY(-3px);
}

/* Floating Image */
.floating-girl {
  animation: gentleFloat 6s ease-in-out infinite;
  border-radius: 1rem;
  filter: drop-shadow(0 10px 25px rgba(0, 0, 0, 0.15));
}
@keyframes gentleFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Features */
.feature-card {
  border: 1px solid #e3f2fd;
  transition: all 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}
.floating-icon {
  animation: floatIcon 3s ease-in-out infinite;
}
@keyframes floatIcon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* Stats  */
.stats-section h2 {
  animation: fadeIn 1.2s ease-in;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Trusted Companies  */
.trusted-logos {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2.5rem;
}

.logo-card {
  background: #fff;
  border-radius: 1rem;
  width: 160px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 20px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.logo-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.company-logo {
  max-width: 100px;
  max-height: 50px;
  object-fit: contain;
  filter: grayscale(100%) brightness(0.9);
  opacity: 0.85;
  transition: all 0.3s ease;
}
.company-logo:hover {
  filter: none;
  opacity: 1;
  transform: scale(1.1);
}

/*  Responsive */
@media (max-width: 992px) {
  .logo-card {
    width: 130px;
    height: 80px;
  }
  .company-logo {
    max-width: 80px;
    max-height: 40px;
  }
}

@media (max-width: 576px) {
  .logo-card {
    width: 110px;
    height: 70px;
  }
  .trusted-logos {
    gap: 1.5rem;
  }
}

/* Testimonial Section */
.testimonial-section {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  overflow: hidden;
}

.testimonial-slider {
  display: flex;
  gap: 2rem;
  animation: slideLeft 28s linear infinite;
  width: max-content;
}

.testimonial-card {
  min-width: 300px;
  max-width: 350px;
  text-align: left;
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

@keyframes slideLeft {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
