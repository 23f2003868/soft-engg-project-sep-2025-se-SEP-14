<template>

  <Navbar />

  <section class="contact-section py-5">
    <div class="container">
      <!-- Header -->
      <div class="text-center mb-5" data-aos="fade-up">
        <h2 class="fw-bold text-primary mb-2">Contact Us</h2>
        <p class="text-muted fs-5">
          Have questions or feedback? We'd love to hear from you!
        </p>
      </div>

      <div class="row g-4 align-items-center">
        <!-- Contact Info -->
        <div class="col-lg-5" data-aos="fade-right">
          <div class="info-card p-4 rounded-4 shadow-sm bg-white h-100">
            <h5 class="fw-bold text-dark mb-3">Get in Touch</h5>
            <p class="text-secondary mb-4">
              Our support team is here to assist you with queries related to jobs, accounts, or partnerships.
            </p>

            <ul class="list-unstyled mb-4">
              <li class="mb-3">
                <i class="bi bi-geo-alt-fill text-primary me-2"></i>
                <span>123 Innovation Street, Gurugram, India</span>
              </li>
              <li class="mb-3">
                <i class="bi bi-envelope-fill text-primary me-2"></i>
                <span>support@jobportal.com</span>
              </li>
              <li>
                <i class="bi bi-telephone-fill text-primary me-2"></i>
                <span>+91 98011 00000</span>
              </li>
            </ul>

            <div class="d-flex gap-3">
              <a href="#" class="social-icon text-primary fs-4"><i class="bi bi-facebook"></i></a>
              <a href="#" class="social-icon text-primary fs-4"><i class="bi bi-twitter-x"></i></a>
              <a href="#" class="social-icon text-primary fs-4"><i class="bi bi-linkedin"></i></a>
              <a href="#" class="social-icon text-primary fs-4"><i class="bi bi-instagram"></i></a>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="col-lg-7" data-aos="fade-left">
          <div class="contact-form-card p-4 rounded-4 shadow-sm bg-white">
            <form @submit.prevent="handleSubmit">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-medium">Full Name</label>
                  <input 
                    type="text" 
                    v-model="name" 
                    class="form-control" 
                    placeholder="Your Name"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-medium">Email Address</label>
                  <input 
                    type="email" 
                    v-model="email" 
                    class="form-control" 
                    placeholder="name@example.com"
                    required
                  />
                </div>
              </div>

              <div class="mt-3">
                <label class="form-label fw-medium">Subject</label>
                <input 
                  type="text" 
                  v-model="subject" 
                  class="form-control" 
                  placeholder="How can we help you?"
                  required
                />
              </div>

              <div class="mt-3">
                <label class="form-label fw-medium">Message</label>
                <textarea 
                  v-model="message" 
                  rows="4" 
                  class="form-control" 
                  placeholder="Write your message here..."
                  required
                ></textarea>
              </div>

              <div v-if="successMessage" class="alert alert-success mt-3 py-2 text-center">
                {{ successMessage }}
              </div>

              <button 
                type="submit" 
                class="btn btn-primary w-100 fw-bold mt-4 py-2"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? 'Sending...' : 'Send Message' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Google Map Section -->
      <div class="map-container mt-5" data-aos="fade-up">
        <iframe
          class="map-frame rounded-4 shadow-sm"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3500.983377994241!2d77.04104507457676!3d28.67196997565919!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390d046b7bbba7db%3A0x2398b1a957d1823c!2sGurugram%2C%20Haryana!5e0!3m2!1sen!2sin!4v1704972378325!5m2!1sen!2sin"
          width="100%"
          height="400"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>
    </div>
  </section>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import { ref, onMounted } from 'vue';
import AOS from 'aos';
import 'aos/dist/aos.css';

const name = ref('');
const email = ref('');
const subject = ref('');
const message = ref('');
const isSubmitting = ref(false);
const successMessage = ref('');

onMounted(() => {
  AOS.init({
    duration: 1000,
    once: true,
    easing: 'ease-in-out',
  });
});

const handleSubmit = () => {
  if (!name.value || !email.value || !subject.value || !message.value) return;

  isSubmitting.value = true;
  successMessage.value = '';

  setTimeout(() => {
    isSubmitting.value = false;
    successMessage.value = 'Your message has been sent successfully!';
    name.value = '';
    email.value = '';
    subject.value = '';
    message.value = '';
  }, 1500);
};
</script>

<style scoped>
.contact-section {
  background-color: #f8f9fa;
}

.info-card,
.contact-form-card {
  transition: all 0.3s ease;
}

.info-card:hover,
.contact-form-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.1);
}

.form-control:focus {
  box-shadow: 0 0 0 0.15rem rgba(13, 110, 253, 0.25);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Social Icon Hover Colors */
.social-icon:hover {
  transform: scale(1.15);
  transition: all 0.3s ease;
}

.social-icon:nth-child(1):hover {
  color: #1877f2 !important; /* Facebook */
}
.social-icon:nth-child(2):hover {
  color: #000000 !important; /* X (Twitter) */
}
.social-icon:nth-child(3):hover {
  color: #0a66c2 !important; /* LinkedIn */
}
.social-icon:nth-child(4):hover {
  color: #e4405f !important; /* Instagram */
}

/* Map Styling */
.map-container {
  margin-top: 60px;
}

.map-frame {
  width: 100%;
  height: 400px;
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .map-frame {
    height: 300px;
  }
}
</style>
