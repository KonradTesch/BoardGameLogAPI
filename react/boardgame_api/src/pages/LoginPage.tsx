import InputField from "../components/InputField.tsx";
import Button from "../components/Button/Button.tsx";
import LoginCard from "../components/Cards/LoginCard.tsx";
import {useContext, useEffect, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import InformationText from "../components/Text/InformationText.tsx";
import type {InfoText} from "../types/InfoText.ts";
import {getDetailStringOrDefault} from "../util/util.ts";
import {ROUTES} from "../types/routes.ts";
import type {User} from "../types/User.ts";
import {useToast} from "../context/ToastContext.tsx";
import {Navigate} from "react-router-dom";

function LoginPage() {

    const {user, setUser} = useContext(AuthContext)!;
    const {showToast} = useToast();

    const [isLogin, setIsLogin] = useState(true);
    const [infoMessage, setInfoMessage] = useState<InfoText | null>(null);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    useEffect(() => {
        if (isLogin && confirmPassword !== "" && password !== "" && confirmPassword !== password) {
            setInfoMessage({message: "Passwords do not match", variant: "warning"});
        } else {
            setInfoMessage({message: ""});
        }
    }, [password, confirmPassword])

    if (user) return <Navigate to={ROUTES.dashboard.to(user.id)} replace />;

    const isValidInput = username !== "" && password !== "" && (isLogin || confirmPassword !== "");

    const toggleLogin = () => {
        setIsLogin(!isLogin);
    };

    const handleSignup = async () => {
        try {
            const response = await fetch("/api/auth/register", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: username, password: password})
            });
            const data = await response.json();
            if (response.ok) {
                setInfoMessage({message: data.message, variant: "success"})
                await handleLogin();
            } else {
                setInfoMessage({message: getDetailStringOrDefault(data.detail, "Unknown error"), variant: "warning"})
            }
        }
        catch {
            showToast({message: "Register failed. The server is not responding.", variant: "danger"})
        }

    };

    const handleLogin = async () => {
        try {
            const formData = new URLSearchParams();
            formData.append("username", username);
            formData.append("password", password);

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: formData
            });

            if (response.ok) {
                const userResponse: User = await response.json();
                showToast({message: "Login successful", variant: "success"})

                setUser(userResponse);
            } else {
                const failedResponse = await response.json();
                setInfoMessage({
                    message: getDetailStringOrDefault(failedResponse, "Unknown error, try again later."),
                    variant: "warning"
                })
            }
        } catch {
            showToast({message: "Login failed. The server is not responding.", variant: "danger"})
        }
    };

    return (
        <LoginCard isLogin={isLogin}>
            <div className={"d-flex flex-column gap-3"}>
                <InputField
                    label="Username:"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <InputField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                {!isLogin && <InputField
                    label="Confirm Password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />}
            </div>

            <div className="text-center">
                {infoMessage && <InformationText infoText={infoMessage}/>}
                <Button
                    variant="primary"
                    label={isLogin ? "Login" : "Register"}
                    onClick={isLogin ? handleLogin : handleSignup}
                    disabled={!isValidInput}
                />
                <p className="mt-2"> {isLogin ? "No account yet?" : "Already have an account?"} <span
                    className="fw-bold toggle-link" onClick={toggleLogin}>{isLogin ? "Register" : "Login"} here</span>
                </p>
            </div>
        </LoginCard>
    );
}

export default LoginPage;