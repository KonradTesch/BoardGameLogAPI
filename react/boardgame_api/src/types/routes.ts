export const ROUTES = {
    login: {
        path: '/login',
        to: '/login'
    },
    dashboard: {
        path: "/user/:userId/dashboard",
        to: (userId: number) => `/user/${userId}/dashboard`
    },
    accountSettings: {
        path: "/user/:userId/settings",
        to: (userId: number) => `/user/${userId}/settings`
    },
    editSessions: {
        path: "/user/:userId/sessions/edit",
        to: (userId: number) => `/user/${userId}/sessions/edit`
    }
}