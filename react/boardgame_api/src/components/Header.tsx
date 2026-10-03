import { useState, useEffect, useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import NavDropdown from "./Dropdowns/NavDropdown.tsx";
import Button from "./Button/Button.tsx";
import {Link, useNavigate} from "react-router-dom";
import {ROUTES} from "../types/routes.ts";
import {useToast} from "../context/ToastContext.tsx";

function Header() {
    const navigate = useNavigate();

    const { user, setUser } = useContext(AuthContext)!;
    const { showToast } = useToast();

    const [isDark, setIsDark] = useState(
        () => localStorage.getItem("theme") === "dark"
    );

    useEffect (() => {
       const theme = isDark ? "dark" : "light";
       document.documentElement.setAttribute('data-bs-theme', theme);
       localStorage.setItem("theme", theme)
    }, [isDark]);

    const handleLogout = async () => {
        try {
            const response = await fetch(`/api/auth/logout`, {
                method: "POST",
                credentials: "include"
            });

            if (response.ok) {
                setUser(null)
                navigate(ROUTES.login.to)
            } else {
                showToast({ message: `Logout failed, try again later (${response.status}).`, variant: "danger" });
            }
        }
        catch {
            showToast({ message: `Logout failed. The server is not responding.`, variant: "danger" });
        }
    }

    return (
        <>
            <nav className="navbar bg-body-tertiary">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        <i className="bi bi-dice-6-fill" /> Boardgame Log API
                    </a>
                    <div className="d-flex align-items-center gap-4">
                        {user && <NavDropdown user={user} dropdownOptions={[
                            <Link className="dropdown-item" to={ROUTES.dashboard.to(user.id)}>Dashboard</Link>,
                            <Link className="dropdown-item" to={ROUTES.accountSettings.to(user.id)}>Account Settings</Link>,
                            <div className="dropdown-item">
                                <Button label="Logout" onClick={handleLogout}/>
                            </div>
                        ]}/>}
                        <button onClick={() => setIsDark(!isDark)}>
                            <i className={isDark ? 'bi bi-sun-fill' : 'bi bi-moon-fill'}></i>
                        </button>
                    </div>
                </div>
            </nav>
        </>
    );
}

export default Header;