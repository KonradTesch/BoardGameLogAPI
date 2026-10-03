import {useContext, useEffect} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import type {User} from "../types/User.ts";

function AppAuth() {

    const { setUser, setIsLoading } = useContext(AuthContext)!;

    useEffect(() => {
        const auth_user = async () => {
            const response = await fetch("/api/auth/user", {
            method: "GET",
            });
            setIsLoading(false);
            if (response.ok){
                const data: User = await response.json();
                setUser(data)
            }
            else
            {
                setUser(null);
            }
        }
        void auth_user();
    }, []);

    return <></>;
}

export default AppAuth;