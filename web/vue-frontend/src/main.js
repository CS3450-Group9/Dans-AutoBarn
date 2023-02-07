import { createApp } from 'vue'
import router from './router'; // import our router
import App from './App.vue'

createApp(App).mount('#app')

const app = createApp(App); // create our app instance

app.use(router); // tell our app to use our router

app.mount("#app"); // mount our app on the div#app element in our template