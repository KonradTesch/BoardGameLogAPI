import {Navigate, Route, Routes} from "react-router-dom";
import Header from "../components/Text/Header.tsx";
import LoginPage from "../pages/LoginPage.tsx";
import DashboardPage from "../pages/DashboardPage.tsx";
import {useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import AccountSettingsPage from "../pages/AccountSettingsPage.tsx";
import EditSessionPage from "../pages/EditSessionPage.tsx";
import {ROUTES} from "../types/routes.ts";

function AppContent() {
    const { isLoading } = useContext(AuthContext)!;

    if (isLoading) return <div>Loading...</div>;

    return (
        <>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path={ROUTES.login.path} element={<LoginPage />} />
                <Route path={ROUTES.dashboard.path} element={<DashboardPage />} />
                <Route path={ROUTES.accountSettings.path} element={<AccountSettingsPage />} />
                <Route path={ROUTES.editSessions.path} element={<EditSessionPage />} />
            </Routes>
        </>
    );
}

export default AppContent;