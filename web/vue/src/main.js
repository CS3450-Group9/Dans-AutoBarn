import axios from 'axios';
import VueAxios from 'vue-axios';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

app.use(router);
app.use(VueAxios, axios);

createApp(App).mount('#app');
