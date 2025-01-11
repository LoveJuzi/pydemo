import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/home',
        name: 'Home',
        component: () => import('../components/HomePage.vue'),
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../components/AboutPage.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
