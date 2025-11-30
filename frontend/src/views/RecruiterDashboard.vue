<template>
  <div class="d-flex">
    <div class="flex-grow-1">
      <Topbar />

      <main class="p-4">
        <JobsTable />
      </main>
    </div>
  </div>
</template>

<script setup>
import Topbar from "../components/RecruiterNavbar.vue";
import JobsTable from "../components/JobManagement.vue";
</script>

