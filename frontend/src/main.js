// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import Home from './components/Home';
import Default from './components/Default';
import Register from './components/Register';
import VueRouter from 'vue-router';
import { routes } from './routes';
import VueResource from 'vue-resource';

Vue.config.productionTip = false;
Vue.use(VueResource);
Vue.use(VueRouter);

const router = new VueRouter({
  routes: routes,
  mode: 'history',
});

/* eslint-disable no-new */
new Vue({
  router: router,
  render: h => h(App),
}).$mount('#app');
