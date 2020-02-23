import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Trucks from '../views/Trucks.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/trucks',
    name: 'Trucks',
    component: Trucks,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
