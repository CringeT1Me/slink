import { createApp } from 'vue';
import App from './App.vue';
import router from './router.js';
import store from './store.js';

const app = createApp(App);

app.use(store);  // Подключение Vuex Store
app.use(router); // Подключение Vue Router

app.mount('#app');