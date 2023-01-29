import { createWebHistory, createRouter } from "vue-router";

import temp from "./apps/temp.vue"

const routes = [
    {
        path: '/temp',
        component: temp
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

export default router;