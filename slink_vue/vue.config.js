const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    host: 'localhost',
    port: 8080,
    // https: {
    //   key: fs.readFileSync('./certs//localhost+2-key.pem'),
    //   cert: fs.readFileSync('./certs//localhost+2.pem'),
    //   //ca: fs.readFileSync('./certs/my-ca.crt')
    // },
  }
};
