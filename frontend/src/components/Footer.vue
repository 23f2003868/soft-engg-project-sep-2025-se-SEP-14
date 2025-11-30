<template>
  <footer
    class="footer-section text-light py-5 mt-auto position-relative overflow-hidden"
  >
    <!-- Soft gradient and floating bubbles for consistency with Hero -->
    <div class="footer-gradient"></div>
    <div class="footer-bubbles">
      <div v-for="n in 12" :key="n" class="bubble"></div>
    </div>

    <div class="container-lg position-relative" style="z-index: 2;">
      <div class="footer-flex">
        <!-- Brand Section -->
        <div class="footer-column">
          <h4 class="fw-bold text-accent mb-3">ApplAI</h4>
          <p class="small opacity-75 mb-1">
            © {{ new Date().getFullYear() }} ApplAI
          </p>
          <p class="small opacity-75 mb-0">
            Connecting people with the right opportunities using smart AI tools.
          </p>
        </div>

        <!-- Links Section -->
        <div class="footer-column">
          <h6 class="fw-semibold text-accent mb-3">Quick Links</h6>
          <ul class="list-unstyled small mb-0">
            <li>
              <router-link to="/jobs" class="footer-link">Browse Jobs</router-link>
            </li>
            <li>
              <router-link to="/contact" class="footer-link">Contact Us</router-link>
            </li>
          </ul>
        </div>

        <!-- Social Section -->
        <div class="footer-column">
          <h6 class="fw-semibold text-accent mb-3">Follow Us</h6>
          <div class="social-icons">
            <a href="#" class="footer-icon"><i class="bi bi-facebook"></i></a>
            <a href="#" class="footer-icon"><i class="bi bi-twitter-x"></i></a>
            <a href="#" class="footer-icon"><i class="bi bi-linkedin"></i></a>
            <a href="#" class="footer-icon"><i class="bi bi-instagram"></i></a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
:root {
  --accent-color: #00c6ff;
}

/* ---------- Footer Section ---------- */
.footer-section {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  overflow: hidden;
  position: relative;
  text-align: center;
}

/* Centered Layout with Equal Space */
.footer-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2.5rem;
}

.footer-column {
  flex: 1;
  min-width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Accent Color */
.text-accent {
  color: var(--accent-color);
}

/* Footer Links */
.footer-link {
  color: #cfd8dc;
  text-decoration: none;
  display: inline-block;
  margin-bottom: 6px;
  transition: all 0.3s ease;
}
.footer-link:hover {
  color: var(--accent-color);
  transform: translateX(5px);
}

/* Social Icons */
.social-icons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}
.footer-icon {
  color: #cfd8dc;
  font-size: 1.6rem;
  transition: all 0.3s ease;
}
.footer-icon:hover {
  color: var(--accent-color);
  transform: scale(1.25);
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
}

/* ---------- Background Styling ---------- */
.footer-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(
      circle at top left,
      rgba(0, 198, 255, 0.15),
      transparent 70%
    ),
    radial-gradient(circle at bottom right, rgba(0, 198, 255, 0.15), transparent 70%);
  z-index: 1;
}

.footer-bubbles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}
.bubble {
  position: absolute;
  bottom: -60px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  animation: bubbleUp 18s infinite ease-in;
}
.bubble:nth-child(1) { width: 16px; height: 16px; left: 10%; animation-duration: 14s; }
.bubble:nth-child(2) { width: 22px; height: 22px; left: 30%; animation-duration: 17s; }
.bubble:nth-child(3) { width: 20px; height: 20px; left: 50%; animation-duration: 19s; }
.bubble:nth-child(4) { width: 26px; height: 26px; left: 70%; animation-duration: 21s; }
.bubble:nth-child(5) { width: 18px; height: 18px; left: 85%; animation-duration: 16s; }

@keyframes bubbleUp {
  0% { transform: translateY(0) scale(1); opacity: 0.3; }
  50% { opacity: 0.8; }
  100% { transform: translateY(-900px) scale(1.4); opacity: 0; }
}

/* ---------- Responsive ---------- */
@media (max-width: 768px) {
  .footer-flex {
    flex-direction: column;
    text-align: center;
  }
  .social-icons {
    gap: 1rem;
  }
}
</style>
