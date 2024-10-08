<template>
  <div class="container">
    <h2>Регистрация</h2>
    <form v-if="!registrationComplete" @submit.prevent="submitForm">
      <label for="first_name">Имя:</label>
      <input type="text" id="first_name" v-model="first_name" required>

      <label for="last_name">Фамилия:</label>
      <input type="text" id="last_name" v-model="last_name" required>

      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required>

      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" @input="validateEmail" required>
      <span v-if="emailError" class="error">{{ emailError }}</span>

      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" @input="validatePassword" required>

      <label for="confirmPassword">Confirm Password:</label>
      <input type="password" id="confirmPassword" v-model="confirmPassword" @input="validatePassword" required>
      <span v-if="passwordError" class="error">{{ passwordError }}</span>

      <button type="submit" :disabled="emailError || passwordError || isLoading">
        {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>
    </form>

    <div v-if="registrationComplete">
      <p class="success">{{ successMessage }}</p>
      <p v-if="countdown > 0">Вы можете повторно отправить письмо через {{ countdown }} секунд.</p>
      <button v-else @click="resendActivationEmail" :disabled="isLoading">
        {{ isLoading ? 'Отправка...' : 'Отправить повторно' }}
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
const first_name = ref('');
const last_name = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const emailError = ref('');
const passwordError = ref('');
const isLoading = ref(false);
const successMessage = ref('');
const registrationComplete = ref(false);
const countdown = ref(30);

const validateEmail = () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  emailError.value = emailPattern.test(email.value) ? '' : 'Введите корректный email.';
  console.log('Email:', email.value, 'Email Error:', emailError.value); // Логирование email и ошибок
};

const validatePassword = () => {
  passwordError.value = password.value !== confirmPassword.value ? 'Пароли не совпадают.' : '';
  console.log('Password:', password.value, 'Confirm Password:', confirmPassword.value, 'Password Error:', passwordError.value); // Логирование паролей и ошибок
};

const startCountdown = () => {
  const interval = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);
};

const submitForm = async () => {
  if (emailError.value || passwordError.value) {
    return;
  }

  isLoading.value = true;

  const data = {
    first_name: first_name.value,
    last_name: last_name.value,
    username: username.value,
    email: email.value,
    password: password.value,
  };

  try {
    const response = await fetch('http://localhost:8000/api/v1/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    if (response.ok) {
      successMessage.value = 'Регистрация успешна! Проверьте вашу почту для подтверждения.';
      registrationComplete.value = true;
      startCountdown();
    } else {
      console.error('Ошибка:', result);
    }
  } catch (error) {
    console.error('Ошибка при отправке формы:', error);
  } finally {
    isLoading.value = false;
  }
};

const resendActivationEmail = async () => {
  isLoading.value = true;

  try {
    const response = await fetch('http://localhost:8000/api/v1/users/resend_activation/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email.value }),
    });

    if (response.ok) {
      successMessage.value = 'Письмо было повторно отправлено на вашу почту.';
      countdown.value = 30;
      startCountdown();
    } else {
      const result = await response.json();
      console.error('Ошибка:', result);
    }
  } catch (error) {
    console.error('Ошибка при повторной отправке письма:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 300px;
    text-align: center;
}

h2 {
    margin-bottom: 20px;
}

form {
    display: flex;
    flex-direction: column;
}

label {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="text"],
input[type="email"],
input[type="password"] {
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    padding: 10px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #218838;
}

p {
    margin-top: 20px;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
.error {
    color: red;
    font-size: 12px;
}

input.invalid {
    border-color: red;
}
</style>
