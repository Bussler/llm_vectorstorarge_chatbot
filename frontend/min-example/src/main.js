import './assets/main.css'
//theme
import "primevue/resources/themes/vela-green/theme.css";
//icons
import 'primeicons/primeicons.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'

import PrimeVue from 'primevue/config';
import Button from "primevue/button"
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Divider from 'primevue/divider';
import ProgressSpinner from 'primevue/progressspinner';


const app = createApp(App)

app.use(PrimeVue);
app.use(router);
app.use(VueAxios, axios)

app.component('Button', Button);
app.component('Card', Card);
app.component('InputText', InputText);
app.component('Divider', Divider);
app.component('ProgressSpinner', ProgressSpinner);

app.mount('#app')
