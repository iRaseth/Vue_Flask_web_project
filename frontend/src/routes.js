import Home from './components/Home.vue';
import Register from './components/Register.vue';
import Default from './components/Default.vue';

export const routes = [
  { path: '/', component:  Home },
  { path: '/default', component: Default },
  { path: '/register', component: Register },
  { path: '/redirect-me', redirect: '/default' }
];
