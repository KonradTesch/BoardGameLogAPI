import {useContext, useEffect} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {useNavigate} from "react-router-dom";

function AppAuth() {
    const { setUser, setIsLoading } = useContext(AuthContext)!;
    const navigate = useNavigate();

useEffect(() => {
    const auth_user = async () => {
        setIsLoading(true);
        const response = await fetch("/api/auth/user", {
        method: "GET",
        });
        setIsLoading(false);
        if (response.ok){
            const data = await response.json();
            setUser(data)

            navigate(`/user/${data.id}/dashboard`)
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