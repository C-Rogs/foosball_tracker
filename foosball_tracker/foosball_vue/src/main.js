import { createApp } from 'vue';
import App from './App.vue';
import FoodItem from './components/FoodItem.vue'

import router from './router';
import axios from 'axios';

//import './assets/main.css'

// Set the base URL for Axios
axios.defaults.baseURL = 'http://localhost:8000/api/';

const app = createApp(App);
app.component('food-item', FoodItem)

app.use(router);

app.mount('#app');
