<template>
  <div class="container">
    <h2>Подтверждение смены электронной почты</h2>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const message = ref('');
const route = useRoute();
const router = useRouter();

const confirmEmailChange = async (uid, token, encodedNewEmail) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/users/set_email_confirm/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ uid, token, encoded_new_email: encodedNewEmail }),
    });

    if (response.ok) {
      message.value = 'Ваш email успешно изменен! Перенаправление...';
      setTimeout(() => {
        router.push('/');
      }, 3000);
    } else {
      message.value = `Ошибка подтверждения смены email: Неизвестная ошибка`;
    }
  } catch (error) {
    message.value = `Ошибка при подтверждении смены email: ${error.message}`;
  }
};

onMounted(() => {
  const { uid, token, encoded_new_email: encodedNewEmail } = route.params;
  if (uid && token && encodedNewEmail) {
    confirmEmailChange(uid, token, encodedNewEmail);
  } else {
    message.value = 'Неверные параметры подтверждения смены email.';
  }
});
</script>
