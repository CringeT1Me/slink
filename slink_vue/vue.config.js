// vue.config.js
const { defineConfig } = require('@vue/cli-service');
const dotenv = require('dotenv');

// Загрузка переменных окружения
dotenv.config();

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: process.env.FRONTEND_DOMAIN || 'testslink.ru',
    port: process.env.FRONTEND_PORT || 80,
    // host: process.env.FRONTEND_DOMAIN || 'localhost',
    // port: process.env.FRONTEND_PORT || 8080,
    // Если хотите использовать HTTPS:
    // https: {
    //   key: fs.readFileSync('./certs/localhost-key.pem'),
    //   cert: fs.readFileSync('./certs/localhost.pem'),
    // },
  },
});
