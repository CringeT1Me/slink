<template>
  <div class="profile-container">
    <!-- Шапка профиля -->
    <div class="profile-header">
      <div class="avatar-section">
        <img :src="user.avatar_url" alt="Аватар пользователя" class="avatar" />
      </div>
      <div class="user-info">
        <h2 class="username">{{ user.username }}</h2>
        <p class="full-name">{{ user.first_name }} {{ user.last_name }}</p>
        <p class="description">{{ user.description || 'Описание отсутствует' }}</p>
      </div>
      <div class="user-actions">
        <p class="last-seen">Был в сети: {{ lastSeen }}</p>
        <div class="actions-buttons">
          <button class="action-btn">Добавить в друзья</button>
          <button class="action-btn">Написать сообщение</button>
          <button class="action-btn">Подробнее</button>
        </div>
      </div>
    </div>

    <!-- Модальная форма с дополнительной информацией -->
    <div v-if="showMoreInfo" class="more-info-modal">
      <div class="more-info-content">
        <h3>Подробнее</h3>
        <p v-if="user.country_name">Страна: {{ user.country_name }}</p>
        <p v-if="user.city_name">Город: {{ user.city_name }}</p>
        <p>Пол: {{ user.gender || 'Не указан' }}</p>
        <button @click="toggleMoreInfo" class="close-btn">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const showMoreInfo = ref(false);

// Функция для открытия/закрытия формы "Подробнее"
const toggleMoreInfo = () => {
  showMoreInfo.value = !showMoreInfo.value;
};

const user = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  description: '',
  is_active: false,
  city_name: '',
  country_name: '',
  avatar_url: '',
});

const fetchUserProfile = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/users/me/', {
      headers: {
        'Authorization': `Bearer ${store.state.accessToken}`,
      },
    });

    if (response.ok) {
      const userData = await response.json();
      user.value = userData;
    }
    else if (response.status === 401) {
      const refreshed = await store.dispatch("refreshAccessToken");
      if (refreshed) {
        fetchUserProfile();
      } else {
        router.push("/login");
      }
    } else {
      console.error("Ошибка загрузки профиля:", response.statusText);
    }
  } catch (error) {
    console.error("Ошибка загрузки профиля:", error);
  }
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<style scoped>
/* Основной контейнер */
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  position: relative;
}

/* Верхний блок профиля */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Блок с аватаром */
.avatar-section {
  margin-right: 20px;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ddd;
}

/* Информация о пользователе */
.user-info {
  flex-grow: 1;
}

.username {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.full-name {
  font-size: 20px;
  color: #666;
  margin-bottom: 10px;
}

.description {
  font-size: 16px;
  color: #555;
  margin-bottom: 10px;
}

/* Блок действий и последний визит */
.user-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.last-seen {
  font-size: 14px;
  color: #888;
  margin-bottom: 10px;
}

/* Кнопки действий */
.actions-buttons {
  display: flex;
  flex-direction: column;
}

.action-btn {
  padding: 8px 16px;
  background-color: #f1f1f1;
  color: #333;
  border: none;
  border-radius: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #e0e0e0;
}

/* Модальная форма с дополнительной информацией */
.more-info-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.more-info-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  width: 300px;
}

.close-btn {
  padding: 8px 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
}
</style>