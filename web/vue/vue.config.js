const { defineConfig } = require('@vue/cli-service')
module.exports = {
  publicPath: 'http://localhost:8080', // base URL where app will be deployed
  outputDir: '../static/dist', // path where files will be output upon build
  indexPath: '../../templates/home.html', // path for generated index file
  
  configureWebpack: {
    devServer: {
      devMiddleware: {
        writeToDisk: true
      }
    }
  }
}
