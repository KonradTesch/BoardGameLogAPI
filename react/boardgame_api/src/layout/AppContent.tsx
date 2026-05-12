import {Navigate, Route, Routes} from "react-router-dom";
import Header from "../components/Header.tsx";
import LoginPage from "../pages/LoginPage.tsx";
import DashboardPage from "../pages/DashboardPage.tsx";
import {useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";

function AppContent() {
    const { isLoading } = useContext(AuthContext)!;

    if (isLoading) return <div>Loading...</div>;

    return (
        <>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/user/:userId/dashboard" element={<DashboardPage/>} />
            </Routes>
        </>
    );
}

export default AppContent;