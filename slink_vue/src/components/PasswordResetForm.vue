<template>
  <div class="container">
    <h2>Восстановление пароля</h2>
    <form @submit.prevent="submitResetPassword">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" placeholder="Логин, почта или номер телефона" required />

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Отправка...' : 'Отправить' }}
      </button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Поле для ввода username
const username = ref('');

// Состояние загрузки и сообщения об ошибках/успехах
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const submitResetPassword = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const response = await fetch('http://localhost:8000/api/v1/users/reset_password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username.value }),
    });

    if (response.ok) {
      successMessage.value = 'Письмо для сброса пароля отправлено на вашу почту.';
    } else {
      errorMessage.value = 'Ошибка отправки. Проверьте введенные данные.';
    }
  } catch (error) {
    errorMessage.value = 'Ошибка при отправке запроса.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
/* Стили для компонента остаются аналогичными */
</style>
