import {BrowserRouter} from "react-router-dom"
import {AuthProvider} from "./context/AuthContext.tsx";
import AppAuth from "./layout/AppAuth.tsx";
import "./styles/App.css"
import AppContent from "./layout/AppContent.tsx";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <AppAuth />
                <AppContent />
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;