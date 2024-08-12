import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import GameList from './components/GameList.vue';
import GameDetail from './components/GameDetail.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/games', component: GameList },
  { path: '/games/:id', component: GameDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
