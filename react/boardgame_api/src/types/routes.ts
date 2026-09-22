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
        path: "/user/:userId/sessions/:sessionId/edit",
        to: (userId: number, sessionId: number) => `/user/${userId}/sessions/${sessionId}/edit`
    },
    newSession: {
        path: "/user/:userId/sessions/new",
        to: (userId: number) => `/user/${userId}/sessions/new`
    }
}