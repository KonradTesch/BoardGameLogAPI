import { useState, useEffect, useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import NavDropdown from "./NavDropdown.tsx";

function Header() {
    const [isDark, setIsDark] = useState(
        () => localStorage.getItem("theme") === "dark"
    );

    useEffect (() => {
       const theme = isDark ? "dark" : "light";
       document.documentElement.setAttribute('data-bs-theme', theme);
       localStorage.setItem("theme", theme)
    }, [isDark]);

    const { user } = useContext(AuthContext)!;


    return (
        <>
            <nav className="navbar bg-body-tertiary">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        <i className="bi bi-dice-6-fill" /> Boardgame Log API
                    </a>
                    <div className="d-flex align-items-center gap-4">
                        {user && <NavDropdown user={user} dropdownOptions={[
                            <a className="dropdown-item" href="#">User Options</a>,
                            <div className="dropdown-item">
                                <button className="btn btn-primary">Logout</button>
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