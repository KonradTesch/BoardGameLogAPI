import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Header from './components/Header'
import LoginPage from "./pages/LoginPage.tsx";
import "./styles/App.css"
import DashboardPage from "./pages/DashboardPage.tsx";


function App() {
    return (
        <BrowserRouter>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/dashboard" element={<DashboardPage/>} />
            </Routes>

        </BrowserRouter>
    );
}

export default App;