<template>
  <div class="row g-4">
    <div v-for="card in stats" :key="card.title" class="col-md-4">
      <div class="card shadow-sm border-0 p-4 text-center">
        <i :class="`${card.icon} text-primary fs-2 mb-2`"></i>
        <h5>{{ card.title }}</h5>
        <h3 class="fw-bold">{{ card.value }}</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
const stats = [
  { title: "Active Jobs", value: 12, icon: "bi bi-briefcase" },
  { title: "Applications", value: 48, icon: "bi bi-people" },
  { title: "Shortlisted", value: 8, icon: "bi bi-check2-circle" },
];
</script>
