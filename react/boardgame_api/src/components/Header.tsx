import { useState, useEffect } from "react";

function Header() {
    const [isDark, setIsDark] = useState(
        () => localStorage.getItem("theme") === "dark"
    );

    useEffect (() => {
       const theme = isDark ? "dark" : "light";
       document.documentElement.setAttribute('data-bs-theme', theme);
       localStorage.setItem("theme", theme)
    }, [isDark]);


    return (
        <>
            <nav className="navbar bg-body-tertiary">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        <i className="bi bi-dice-6-fill" /> Boardgame Log API
                    </a>
                    <button onClick={() => setIsDark(!isDark)}>
                        <i className={isDark ? 'bi bi-sun-fill' : 'bi bi-moon-fill'}></i>
                    </button>
                </div>
            </nav>
        </>
    );
}

export default Header;