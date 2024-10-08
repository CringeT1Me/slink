<template>
  <div class="edit-profile-container">
    <h2>Редактирование профиля</h2>
    <div>
      <button
        :class="tab === 'profile' ? 'active-tab' : ''"
        @click="tab = 'profile'"
      >
        Информация о пользователе
      </button>
      <button
        :class="tab === 'security' ? 'active-tab' : ''"
        @click="tab = 'security'"
      >
        Безопасность и вход
      </button>
    </div>

    <!-- Вкладка "Информация о пользователе" -->
    <form v-if="tab === 'profile'" @submit.prevent="submitForm">
      <div class="edit-field">
        <label for="avatar">Аватар:</label>
        <div class="avatar-container">
          <img
            :src="avatarPreviewURL || user.avatarURL"
            alt="Аватар"
            class="avatar"
            @click="triggerFileInput"
          />
          <input type="file" id="avatar" ref="fileInput" @change="onFileChange" style="display: none" />
        </div>
      </div>

      <div class="edit-field">
        <label for="firstName">Имя:</label>
        <input type="text" id="firstName" v-model="user.firstName" required />
      </div>

      <div class="edit-field">
        <label for="lastName">Фамилия:</label>
        <input type="text" id="lastName" v-model="user.lastName" required />
      </div>

      <div class="edit-field">
        <label for="country">Страна:</label>
        <input
          type="text"
          id="country"
          v-model="user.countryName"
          @input="fetchCountries"
          @blur="hideCountryDropdown"
          placeholder="Не выбрано"
        />
        <ul v-if="showCountryDropdown" class="dropdown-list">
          <li
            v-for="country in filteredCountries"
            :key="country.id"
            @click="selectCountry(country)"
          >
            {{ country.name }}
          </li>
        </ul>
      </div>

      <div class="edit-field">
        <label for="city">Город:</label>
        <input
          type="text"
          id="city"
          v-model="user.cityName"
          @input="fetchCities"
          @blur="hideCityDropdown"
          placeholder="Не выбрано"
        />
        <ul v-if="showCityDropdown" class="dropdown-list">
          <li
            v-for="city in filteredCities"
            :key="city.id"
            @click="selectCity(city)"
          >
            {{ city.display_name }}
          </li>
        </ul>
      </div>

      <div class="edit-field">
        <label for="description">Описание:</label>
        <textarea id="description" v-model="user.description"></textarea>
      </div>

      <button type="submit" class="btn-save">Сохранить изменения</button>
    </form>

    <!-- Вкладка "Безопасность и вход" -->
    <div v-if="tab === 'security'">
      <div class="edit-field">
        <label>Юзернейм:</label>
        <div class="input-link-container">
          <span>{{ user.username }}</span>
          <a href="#" @click.prevent="changeUsername">Сменить юзернейм</a>
        </div>
      </div>

      <div class="edit-field">
        <label>Емейл:</label>
        <div class="input-link-container">
          <span>{{ user.email }}</span>
          <a href="#" @click.prevent="changeEmail">Сменить емейл</a>
        </div>
      </div>

      <div class="edit-field">
        <label>Номер телефона:</label>
        <div class="input-link-container">
          <span>{{ user.phone }}</span>
          <a href="#" @click.prevent="changePhone">Сменить номер телефона</a>
        </div>
      </div>

      <div class="edit-field">
        <label>Пароль:</label>
        <div class="input-link-container">
          <span></span>
          <a href="#" @click.prevent="changePassword">Сменить пароль</a>
        </div>
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

const tab = ref('profile');

const user = ref({
  avatarURL: null,
  avatarImage: null,
  firstName: "",
  lastName: "",
  city: "",
  country: "",
  description: "",
  countryName: "",
  cityName: "",

});
const avatarPreviewURL = ref(null);
const filteredCountries = ref([]);
const filteredCities = ref([]);
const showCountryDropdown = ref(false);
const showCityDropdown = ref(false);
const fileInput = ref(null);

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    user.value.avatarImage = file; // Устанавливаем файл как новый аватар
    avatarPreviewURL.value = URL.createObjectURL(file); // Создаем временный URL для предпросмотра
  }
};

const triggerFileInput = () => {
  fileInput.value.click(); // Открываем диалог выбора файла
};

const fetchCountries = async () => {
  if (user.value.countryName.length < 2) {
    user.value.country = null;
    filteredCountries.value = null;
    showCountryDropdown.value = false;
    return;
  }

  const response = await fetch(`http://localhost:8000/api/v1/countries/?q=${user.value.countryName}`);
  if (response.ok) {
    const countries = await response.json();
    filteredCountries.value = countries.slice(0, 5);
    showCountryDropdown.value = true;
  }
};

const fetchCities = async () => {
  if (user.value.cityName.length < 2) {
    filteredCities.value = [];
    showCityDropdown.value = false;
    return;
  }
  let response = null;
  if (user.value.country) {
    response = await fetch(`http://localhost:8000/api/v1/cities/?country_id=${user.value.country}&q=${user.value.cityName}`);
  }
  else {
    response = await fetch(`http://localhost:8000/api/v1/cities/?q=${user.value.cityName}`);
  }
  if (response.ok) {
    const cities = await response.json();
    filteredCities.value = cities.slice(0, 5);
    showCityDropdown.value = true;
  }
};

const selectCountry = (country) => {
  user.value.country = country.id;
  user.value.countryName = country.name;
  showCountryDropdown.value = false;
  user.value.city = "";
  user.value.cityName = "";
  filteredCities.value = [];
};

const selectCity = (city) => {
  user.value.city = city.id;
  user.value.cityName = city.display_name;
  showCityDropdown.value = false;
};

const hideCountryDropdown = () => {
  setTimeout(() => (showCountryDropdown.value = false), 200);
};

const hideCityDropdown = () => {
  setTimeout(() => (showCityDropdown.value = false), 200);
};

const initialUser = ref({}); // Для хранения исходных данных

const fetchUserProfile = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/users/me/', {
      headers: {
        'Authorization': `Bearer ${store.state.accessToken}`,
      },
    });

    if (response.ok) {
      const userData = await response.json();
      user.value = {
        avatarURL: userData.avatar_url,
        firstName: userData.first_name,
        lastName: userData.last_name,
        city: userData.city, // ID города
        country: userData.country, // ID страны
        description: userData.description,
        username: userData.username,
        email: userData.email,
        phone: userData.phone,
        countryName: userData.country_name, // Отображаемое название страны
        cityName: userData.city_name, // Отображаемое название города
      };

      initialUser.value = JSON.parse(JSON.stringify(user.value));
    } else if (response.status === 401) {
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

const submitForm = async () => {
  try {
    const formData = new FormData();

    if (user.value.firstName !== initialUser.value.firstName) {
      formData.append("first_name", user.value.firstName);
    }
    if (user.value.lastName !== initialUser.value.lastName) {
      formData.append("last_name", user.value.lastName);
    }
    if (user.value.city !== initialUser.value.city) {
      formData.append("city", user.value.city);
    }
    if (user.value.country !== initialUser.value.country) {
      formData.append("country", user.value.country);
    }
    if (user.value.description !== initialUser.value.description) {
      formData.append("description", user.value.description);
    }

    if (user.value.avatarImage) {
      formData.append("avatar_file", user.value.avatarImage); // Добавляем новый аватар, если он был выбран
    }

    const response = await fetch('http://localhost:8000/api/v1/users/me/', {
      method: "PATCH",
      headers: {
        'Authorization': `Bearer ${store.state.accessToken}`,
      },
      body: formData,
    });

    if (response.ok) {
      console.log("Профиль обновлен успешно!");
      fetchUserProfile(); // Перезагружаем данные после успешного обновления
    } else {
      console.error("Ошибка при обновлении профиля:", response.statusText);
    }
  } catch (error) {
    console.error("Ошибка при обновлении профиля:", error);
  }
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<style scoped>
.edit-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background-color: #f1f1f1;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px 5px 0 0;
}

.tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.edit-field {
  margin-bottom: 15px;
}

.edit-field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.edit-field input,
.edit-field textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.readonly-input {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.input-link-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-link-container a {
  margin-left: 10px;
  color: #4CAF50;
  text-decoration: none;
  font-size: 14px;
}

.input-link-container a:hover {
  text-decoration: underline;
}

.btn-save {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 16px;
}
.edit-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background-color: #f1f1f1;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px 5px 0 0;
}

.tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.edit-field {
  margin-bottom: 15px;
}

.edit-field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.edit-field input,
.edit-field textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.edit-field input[type="file"] {
  padding: 0;
}

.avatar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid #ccc;
}

.btn-save {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 16px;
}

.dropdown-list {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  max-height: 150px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  z-index: 10;
}

.dropdown-list li {
  padding: 8px;
  cursor: pointer;
}

.dropdown-list li:hover {
  background-color: #f0f0f0;
}
.edit-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background-color: #f1f1f1;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px 5px 0 0;
}

.tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.edit-field {
  margin-bottom: 15px;
}

.edit-field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.edit-field input,
.edit-field textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.readonly-input {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.input-link-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-link-container a {
  margin-left: 10px;
  color: #4CAF50;
  text-decoration: none;
  font-size: 14px;
}

.input-link-container a:hover {
  text-decoration: underline;
}

.btn-save {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 16px;
}
.edit-profile-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
}

button.active-tab {
  font-weight: bold;
  text-decoration: underline;
}

.edit-field {
  position: relative;
  margin-bottom: 15px;
}

.edit-field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

textarea {
  resize: vertical;
}

.btn-save {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.btn-save:hover {
  background-color: #45a049;
}

.avatar-container {
  display: flex;
  align-items: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 20px;
  cursor: pointer;
}

.input-link-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.input-link-container span {
  flex-grow: 1;
  text-align: left;
}

.input-link-container a {
  margin-left: 10px;
  text-decoration: underline;
  cursor: pointer;
}

.readonly-input {
  pointer-events: none;
  background-color: transparent;
  border: none;
}

.dropdown-list {
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  background-color: white;
  position: absolute;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  z-index: 1000;
}

.dropdown-list li {
  padding: 10px;
  cursor: pointer;
}

.dropdown-list li:hover {
  background-color: #f0f0f0;
}

/* Стили для вкладки "Безопасность и вход" */
.edit-field input[readonly] {
  text-align: left;
  pointer-events: none;
  background-color: transparent;
  border: none;
  color: #555;
}

.edit-field input[readonly]:focus {
  outline: none;
  box-shadow: none;
}
</style>