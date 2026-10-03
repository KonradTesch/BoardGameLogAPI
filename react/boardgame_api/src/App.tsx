import {BrowserRouter} from "react-router-dom"
import {AuthProvider} from "./context/AuthContext.tsx";
import AppAuth from "./layout/AppAuth.tsx";
import "./styles/App.css"
import AppContent from "./layout/AppContent.tsx";
import {UserDataProvider} from "./context/UserDataContext.tsx";
import {ToastProvider} from "./context/ToastContext.tsx";

function App() {
    return (
        <ToastProvider>
            <AuthProvider>
                <UserDataProvider>
                    <BrowserRouter>
                        <AppAuth/>
                        <AppContent/>
                    </BrowserRouter>
                </UserDataProvider>
            </AuthProvider>
        </ToastProvider>
    );
}

export default App;