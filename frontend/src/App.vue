<template>
  <Navbar />
  <main class="flex-grow-1">
    <RouterView /> 
  </main>

  <Footer />
</template>

<script setup>
import { RouterView } from 'vue-router';
// import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<style>
/* Basic CSS to ensure the footer sticks to the bottom on short pages */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex-grow: 1; 
}
</style>