import {BrowserRouter} from "react-router-dom"
import {AuthProvider} from "./context/AuthContext.tsx";
import AppAuth from "./layout/AppAuth.tsx";
import "./styles/App.css"
import AppContent from "./layout/AppContent.tsx";
import {UserDateProvider} from "./context/UserDataContext.tsx";

function App() {
    return (
        <AuthProvider>
            <UserDateProvider>
                <BrowserRouter>
                    <AppAuth />
                    <AppContent />
                </BrowserRouter>
            </UserDateProvider>
        </AuthProvider>
    );
}

export default App;