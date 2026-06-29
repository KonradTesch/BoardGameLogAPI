import {BrowserRouter} from "react-router-dom"
import {AuthProvider} from "./context/AuthContext.tsx";
import AppAuth from "./layout/AppAuth.tsx";
import "./styles/App.css"
import AppContent from "./layout/AppContent.tsx";
import {UserDataProvider} from "./context/UserDataContext.tsx";

function App() {
    return (
        <AuthProvider>
            <UserDataProvider>
                <BrowserRouter>
                    <AppAuth />
                    <AppContent />
                </BrowserRouter>
            </UserDataProvider>
        </AuthProvider>
    );
}

export default App;