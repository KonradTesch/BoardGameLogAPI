import {useContext, useEffect} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {useLocation, useNavigate} from "react-router-dom";
import {ROUTES} from "../types/routes.ts";

function AppAuth() {
    const navigate = useNavigate();

    const location = useLocation();

    const { setUser, setIsLoading } = useContext(AuthContext)!;

    useEffect(() => {
        const auth_user = async () => {
            const response = await fetch("/api/auth/user", {
            method: "GET",
            });
            setIsLoading(false);
            if (response.ok){
                const data = await response.json();
                setUser(data)
                if (location.pathname === "/login") {
                    navigate(ROUTES.login.to)
                }
            }
            else
            {
                setUser(null);
                navigate(ROUTES.login.to);
            }
        }
        void auth_user();
    }, []);

    return <></>;
}

export default AppAuth;