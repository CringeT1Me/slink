import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    setRefreshToken(state, token) {
      state.refreshToken = token;
      localStorage.setItem('refreshToken', token);
    },
    clearTokens(state) {
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/users/jwt/create/', credentials);
        commit('setAccessToken', response.data.access);
        commit('setRefreshToken', response.data.refresh);
        return true;
      } catch (error) {
        console.error('Ошибка при авторизации:', error.response || error.message);
        return false;
      }
    },
    async refreshAccessToken({ commit, state }) {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/users/jwt/refresh/', {
          refresh: state.refreshToken,
        });
        commit('setAccessToken', response.data.access);
        return true;
      } catch (error) {
        console.error('Ошибка при обновлении токена:', error.response || error.message);
        commit('clearTokens');
        return false;
      }
    },
    logout({ commit }) {
      commit('clearTokens');
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
});

export default store;