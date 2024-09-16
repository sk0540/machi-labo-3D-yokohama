import { createApp } from 'vue'
import { createPinia } from 'pinia'//データストアにPinia使用
import './style.css'
import App from './App.vue'

createApp(App).use(createPinia()).mount('#app');
