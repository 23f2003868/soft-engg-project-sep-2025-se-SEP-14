<template>
  <div>
    <div class="modal fade" ref="modalRoot" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-md modal-dialog-centered">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">Schedule Interview — {{ candidateName }}</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="hide"></button> 
          </div>

          <div class="modal-body">
            <form @submit.prevent="onSubmit" novalidate>
              <div class="mb-2">
                <label class="form-label small">Date & Time</label>
                <input v-model="start" type="datetime-local" class="form-control" required />
              </div>

              <div class="row g-2">
                <div class="col-6">
                  <label class="form-label small">Duration (min)</label>
                  <input v-model.number="duration" type="number" class="form-control" min="5" required />
                </div>
                <div class="col-6">
                  <label class="form-label small">Mode</label>
                  <select v-model="mode" class="form-select" required>
                    <option value="MEET">Google Meet (online)</option>
                    <option value="OFFLINE">Offline (in-person)</option>
                    <option value="PHONE">Phone</option>
                  </select>
                </div>
              </div>

              <div class="mb-2 mt-2">
                <label class="form-label small">Notes (optional)</label>
                <textarea v-model="notes" class="form-control" rows="3"></textarea>
              </div>

              <div class="d-flex justify-content-end gap-2 mt-3">
                <button type="button" class="btn btn-outline-secondary" @click="hide">Cancel</button>
                <button :disabled="submitting" type="submit" class="btn btn-primary">
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-1"></span>
                  Schedule
                </button>
              </div>
            </form>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';

const props = defineProps({
  candidateName: { type: String, default: "" },
  cjrId: { type: [String, Number], default: null },
  apiBase: { type: String, default: "http://127.0.0.1:5000/api" },
  token: { type: String, default: "" },
  visible: { type: Boolean, required: true } 
});

const emit = defineEmits(['scheduled', 'cancel']);

const modalRoot = ref(null);
let bsModal = null;

const start = ref("");
const duration = ref(30);
const mode = ref("MEET");
const notes = ref("");
const submitting = ref(false);

function ensureBootstrapModal() {
  if (!modalRoot.value) return;
  if (!bsModal) {
    bsModal = new Modal(modalRoot.value, { backdrop: 'static', keyboard: false });
    modalRoot.value.removeEventListener('hidden.bs.modal', onHidden); 
    modalRoot.value.addEventListener('hidden.bs.modal', onHidden);
  }
}

function onHidden() {
  if (props.visible) { 
    emit('cancel');
  }
}

watch(() => props.visible, async (isVisible) => {
  await nextTick();
  ensureBootstrapModal();
  
  if (isVisible && props.cjrId && bsModal) {
    try {
      bsModal.show();
    } catch (e) {
      console.warn("Bootstrap show failed", e);
    }
  }
}, { immediate: true }); 

onUnmounted(() => {
  try {
    if (modalRoot.value) modalRoot.value.removeEventListener('hidden.bs.modal', onHidden);
    if (bsModal) {
      if (props.visible) {
        bsModal.hide(); 
      }
      bsModal.dispose();
      bsModal = null;
    }
  } catch (e) {}
});

const hide = () => {
  try { if (bsModal) bsModal.hide(); } catch(e) {}
  resetForm();
};

function resetForm() {
  start.value = "";
  duration.value = 30;
  mode.value = "MEET";
  notes.value = "";
  submitting.value = false;
}

async function onSubmit() {
  if (!start.value) {
    alert("Please select date & time");
    return;
  }
  submitting.value = true;

  let startIso = start.value;
  
  // 1. Ensure seconds are present: YYYY-MM-DDTHH:MM -> YYYY-MM-DDTHH:MM:00
  if (startIso && startIso.length === 16) { 
     startIso += ":00";
  }


  const payload = {
    start_iso: startIso, // This should now be in "YYYY-MM-DD HH:MM:SS" format
    duration_min: Number(duration.value || 30),
    mode: mode.value,
    notes: notes.value || ""
  };

  try {
    const res = await fetch(`${props.apiBase}/schedule-interview/${props.cjrId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(props.token ? { Authorization: `Bearer ${props.token}` } : {})
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json().catch(()=>({}));
    if (!res.ok || !data.success) {
      // If the backend returns the "Invalid start_iso format" error, the alert will show it.
      alert(data.message || data.error || "Failed to schedule interview");
      submitting.value = false;
      return;
    }

    try { if (bsModal) bsModal.hide(); } catch(e) {}
    emit('scheduled', data);
    resetForm();
  } catch (e) {
    console.error(e);
    alert("Server error while scheduling");
    submitting.value = false;
  }
}
</script>

<style scoped>
.modal-content { border: none; }
</style>