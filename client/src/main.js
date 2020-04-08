import Vue from 'vue';
import VueLayers from 'vuelayers';
import 'vuelayers/lib/style.css';
import router from './router';
import App from './App.vue';

Vue.config.productionTip = false;

Vue.use(VueLayers, {
  dataProjection: 'EPSG:4326',
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
