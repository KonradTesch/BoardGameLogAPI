import { useState, useEffect, useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import NavDropdown from "./NavDropdown.tsx";
import Button from "./Button.tsx";
import {useNavigate} from "react-router-dom";

function Header() {
    const [isDark, setIsDark] = useState(
        () => localStorage.getItem("theme") === "dark"
    );

    const { setUser } = useContext(AuthContext)!;

    useEffect (() => {
       const theme = isDark ? "dark" : "light";
       document.documentElement.setAttribute('data-bs-theme', theme);
       localStorage.setItem("theme", theme)
    }, [isDark]);

    const { user } = useContext(AuthContext)!;
    const navigate = useNavigate();

    const handleLogout = async () => {
        const response = await fetch(`/api/user/${user?.id}/logout`, {
            method: "POST",
            credentials: "include"
        });

        if (response.ok) {
            setUser(null)
            navigate("/login")
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
                            <a className="dropdown-item" href={`/user/${user.id}/dashboard`}>Dashboard</a>,
                            <a className="dropdown-item" href={`/user/${user.id}/settings`}>Account Settings</a>,
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