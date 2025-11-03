<template>
  <div class="d-flex">
    <Sidebar />
    <div class="flex-grow-1">
      <Topbar />

      <main class="p-4">
        <StatsCards />

        <div class="mt-5">
          <JobsTable />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import Topbar from "../components/RecruiterNavbar.vue";
import StatsCards from "../components/RecruiterStatsCards.vue";
import JobsTable from "../components/JobManagement.vue";
</script>

<style scoped>
main {
  background-color: #f8f9fa;
  min-height: 100vh;
}
</style>
