import { createWebHistory, createRouter } from "vue-router";

import LoginPage from "./components/LoginPage.vue";

const routes = [
    {
        path: '/login',
        component: LoginPage
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});


export default router;