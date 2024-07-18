import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
//@ts-ignore



createApp(App).use(createPinia()).mount('#app');
