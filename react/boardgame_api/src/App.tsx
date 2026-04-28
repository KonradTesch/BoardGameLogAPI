import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Header from './components/Header'
import LoginPage from "./pages/LoginPage.tsx";
import "./App.css"


function App() {
    return (
        <BrowserRouter>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>

        </BrowserRouter>
    );
}

export default App;