import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import {AuthProvider} from "./context/AuthContext.tsx";
import Header from './components/Header'
import LoginPage from "./pages/LoginPage.tsx";
import DashboardPage from "./pages/DashboardPage.tsx";
import AppAuth from "./components/AppAuth.tsx";
import "./styles/App.css"


function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <AppAuth />
                <Header />
                <Routes>
                    <Route path="/" element={<Navigate to="/login" />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/user/:userId/dashboard" element={<DashboardPage/>} />
                </Routes>

            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;