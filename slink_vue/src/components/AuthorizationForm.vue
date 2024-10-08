<template>
  <div class="container">
    <h2>Авторизация</h2>
    <form @submit.prevent="submitForm">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" placeholder="Логин, почта, номер телефона" required />

      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Авторизация...' : 'Войти' }}
      </button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <div class="links">
      <a @click="goToResetPassword" class="forgot-password">Забыли пароль?</a>
      <a @click="goToRegistration" class="register-link">Нет аккаунта? Зарегистрируйтесь!</a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

// Поля формы
const username = ref('');
const password = ref('');

// Состояние загрузки и сообщения об ошибках/успехах
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Маршрутизатор и хранилище Vuex
const router = useRouter();
const store = useStore();

const submitForm = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const success = await store.dispatch('login', { username: username.value, password: password.value });

    if (success) {
      successMessage.value = 'Авторизация прошла успешно! Перенаправляем на главную страницу...';

      console.log('Переход на:', `/users/${username.value}`);
      router.push(`/users/${username.value}`); // Перенаправление на страницу профиля пользователя
    } else {
      errorMessage.value = 'Ошибка авторизации. Проверьте введенные данные.';
    }
  } catch (error) {
    errorMessage.value = 'Ошибка авторизации. Проверьте введенные данные.';
  } finally {
    isLoading.value = false;
  }
};

// Переход на страницу восстановления пароля
const goToResetPassword = () => {
  router.push('/reset-password');
};

// Переход на страницу регистрации
const goToRegistration = () => {
  router.push('/registration');
};
</script>

<style>
/* Общие стили для контейнера */
.container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

/* Стили для формы */
form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #28a745;
  outline: none;
}

/* Стили для кнопки */
button[type="submit"] {
  padding: 10px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #218838;
}

button[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Сообщения об ошибках и успехах */
.error {
  color: #e74c3c;
  background-color: #fce4e4;
  border: 1px solid #e74c3c;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

.success {
  color: #2ecc71;
  background-color: #e9f7ef;
  border: 1px solid #2ecc71;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

/* Ссылки "Забыли пароль?" и "Зарегистрируйтесь" */
.links {
  text-align: center;
  margin-top: 15px;
}

.forgot-password,
.register-link {
  color: #28a745;
  text-decoration: none;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
  display: block; /* Центрируем через display block и text-align */
}

.forgot-password:hover,
.register-link:hover {
  text-decoration: underline;
}

/* Адаптивные стили */
@media (max-width: 480px) {
  .container {
    padding: 15px;
  }

  h2 {
    font-size: 20px;
  }

  input[type="text"],
  input[type="password"],
  button[type="submit"] {
    font-size: 14px;
    padding: 8px;
  }

  .forgot-password,
  .register-link {
    font-size: 13px;
  }
}
</style>
