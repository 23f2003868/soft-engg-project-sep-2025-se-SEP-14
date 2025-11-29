<template>
  <div>
    <!-- Floating Chat Button -->
    <button
      class="chatbot-toggle-btn btn btn-primary rounded-circle shadow-lg"
      @click="toggleChat"
    >
      <i class="bi" :class="isOpen ? 'bi-x-lg' : 'bi-chat-dots-fill'"></i>
    </button>

    <!-- Chat Window -->
    <transition name="fade">
      <div v-if="isOpen" class="chatbot-window shadow-lg">
        <div class="chat-header bg-primary text-white d-flex justify-content-between align-items-center px-3 py-2">
          <h6 class="m-0"><i class="bi bi-robot me-2"></i>Career Assistant</h6>
          <button class="btn btn-sm btn-light" @click="clearChat">
            <i class="bi bi-trash"></i>
          </button>
        </div>

        <div class="chat-body p-3" ref="chatBody">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            :class="['message', msg.sender]"
          >
            <div class="message-text">{{ msg.text }}</div>
          </div>
        </div>

        <div class="chat-footer d-flex align-items-center p-2 border-top">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Ask about jobs, resumes, or interview tips..."
            class="form-control me-2"
          />
          <button class="btn btn-primary" @click="sendMessage">
            <i class="bi bi-send"></i>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const isOpen = ref(false);
const messages = ref([
  { text: '👋 Hi! I’m your Career Assistant. How can I help you today?', sender: 'bot' }
]);
const userInput = ref('');
const chatBody = ref(null);

const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) nextTick(() => scrollToBottom());
};

const sendMessage = async () => {
  if (!userInput.value.trim()) return;
  messages.value.push({ text: userInput.value, sender: 'user' });
  const question = userInput.value;
  userInput.value = '';
  await nextTick(() => scrollToBottom());

  // Simulated bot response (replace with backend API later)
  setTimeout(() => {
    const response = getBotResponse(question);
    messages.value.push({ text: response, sender: 'bot' });
    nextTick(() => scrollToBottom());
  }, 600);
};

const getBotResponse = (q) => {
  q = q.toLowerCase();
  if (q.includes('job')) return '🔍 Check the “Recommended Jobs” section for roles that match your profile!';
  if (q.includes('resume')) return '📄 Highlight your top achievements and tailor your resume for each job.';
  if (q.includes('interview')) return '💡 Tip: Practice common questions and research the company culture.';
  return 'I’m here to assist with your career journey — ask me about jobs, resumes, or interviews!';
};

const scrollToBottom = () => {
  if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight;
};

const clearChat = () => {
  messages.value = [
    { text: '👋 Hello again! How can I assist you today?', sender: 'bot' }
  ];
};
</script>

<style scoped>
/* Floating Button */
.chatbot-toggle-btn {
  position: fixed;
  bottom: 25px;
  right: 25px;
  width: 60px;
  height: 60px;
  z-index: 1200;
  font-size: 1.4rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Chat Window */
.chatbot-window {
  position: fixed;
  bottom: 90px;
  right: 25px;
  width: 360px;
  max-height: 500px;
  background: #fff;
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 1200;
  animation: slideUp 0.3s ease-out;
}

/* Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Chat body */
.chat-body {
  flex: 1;
  overflow-y: auto;
  background-color: #fafafa;
  padding: 10px;
  height: 350px;
}

.message {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 8px;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background-color: #0072ff;
  color: #fff;
  border-bottom-right-radius: 0;
}

.message.bot {
  align-self: flex-start;
  background-color: #e9ecef;
  color: #212529;
  border-bottom-left-radius: 0;
}

/* Input area */
.chat-footer input {
  border-radius: 20px;
}
.chat-footer button {
  border-radius: 50%;
}
</style>
