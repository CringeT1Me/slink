<template>
  <div class="chat-container">
    <div class="chat-messages">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <div class="message-content">
          <p><strong>{{ message.user }}:</strong> {{ message.text }}</p>
          <div v-if="message.images.length" class="message-images">
            <img v-for="(image, idx) in message.images" :key="idx" :src="image" alt="image" class="message-image"/>
          </div>
        </div>
        <span class="message-time">{{ new Date(message.created_at).toLocaleString() }}</span>
      </div>
    </div>

    <div class="chat-input">
      <input type="text" v-model="messageText" placeholder="Напишите сообщение..." @keyup.enter="sendMessage" />
      <input type="text" v-model="imageUrl" placeholder="URL изображения" />
      <button @click="sendMessage">Отправить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const messages = ref([]);
const messageText = ref('');
const imageUrl = ref('');
let socket = null;

const connectWebSocket = (chatId) => {
  socket = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}/`);

  socket.onopen = () => {
    console.log("Соединение WebSocket установлено");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.value.push(data);
  };

  socket.onerror = (error) => {
    console.error("Ошибка WebSocket:", error);
  };

  socket.onclose = () => {
    console.log("Соединение WebSocket закрыто");
  };
};

const sendMessage = () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    const userId = store.state.userId;
    const message = {
      user: userId,
      text: messageText.value,
      images: imageUrl.value ? [imageUrl.value] : [],
    };
    socket.send(JSON.stringify(message));
    messageText.value = '';
    imageUrl.value = '';
  }
};

onMounted(() => {
  const chatId = "your_chat_id"; // Подставьте ID вашего чата
  connectWebSocket(chatId);
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  max-height: 400px;
}

.message {
  margin-bottom: 10px;
}

.message-content {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 8px;
  display: inline-block;
}

.message-images {
  margin-top: 5px;
}

.message-image {
  width: 100px;
  height: 100px;
  border-radius: 5px;
  object-fit: cover;
  margin-right: 5px;
}

.message-time {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
}

.chat-input {
  display: flex;
  align-items: center;
}

.chat-input input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-input button:hover {
  background-color: #0056b3;
}
</style>
