import {AuthContext} from "../context/AuthContext.tsx";
import {useContext} from "react";
import {Navigate, Outlet} from "react-router-dom";
import {ROUTES} from "../types/routes.ts";

function RequireAuth() {
    const { user } = useContext(AuthContext)!;

    if (!user) return <Navigate to={ROUTES.login.to} replace />;

    return <Outlet />;
}

export default RequireAuth;