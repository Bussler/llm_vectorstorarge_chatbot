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
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import FileUpload from 'primevue/fileupload';
import ProgressBar from 'primevue/progressbar';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';


const app = createApp(App)

app.use(PrimeVue);
app.use(router);
app.use(VueAxios, axios)
app.use(ToastService)

app.component('Button', Button);
app.component('Card', Card);
app.component('InputText', InputText);
app.component('Divider', Divider);
app.component('ProgressSpinner', ProgressSpinner);
app.component('TabView', TabView);
app.component('TabPanel', TabPanel);
app.component('FileUpload', FileUpload);
app.component('ProgressBar', ProgressBar);
app.component('Toast', Toast);

app.mount('#app')
