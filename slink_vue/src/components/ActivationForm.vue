<template>
  <div class="container">
    <h2>Активация аккаунта</h2>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const message = ref('');
const route = useRoute();
const router = useRouter();

const activateAccount = async (uid, token) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/users/activation/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ uid, token }),
    });

    if (response.ok) {
      message.value = 'Ваш аккаунт успешно активирован! Перенаправление...';
      setTimeout(() => {
        router.push('/');
      }, 3000);
    } else {
      message.value = 'Ошибка активации: Неизвестная ошибка}';
    }
  } catch (error) {
    message.value = `Ошибка при активации: ${error.message}`;
  }
};

onMounted(() => {
  const { uid, token } = route.params;
  if (uid && token) {
    activateAccount(uid, token);
  } else {
    message.value = 'Неверные параметры активации.';
  }
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 15px;
}

p {
  font-size: 18px;
  color: #666;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

p.success {
  color: #28a745;
  border-color: #28a745;
  background-color: #e6f7ee;
}

p.error {
  color: #dc3545;
  border-color: #dc3545;
  background-color: #f8d7da;
}
</style>
