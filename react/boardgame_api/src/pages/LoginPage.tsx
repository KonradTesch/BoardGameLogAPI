import InputField from "../components/InputField.tsx";
import Button from "../components/Button.tsx";
import LoginCard from "../components/LoginCard.tsx";
import {useContext, useEffect, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {useNavigate} from "react-router-dom";
import InformationText from "../components/InformationText.tsx";
import type {InfoText} from "../types/InfoText.ts";
import {getDetailStringOrDefault} from "../util/util.ts";

function LoginPage() {
    const navigate = useNavigate()

    const { setUser } = useContext(AuthContext)!;

    const [isLogin, setIsLogin] = useState(true);
    const [infoMessage, setInfoMessage] = useState<InfoText | null>(null);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    useEffect(() => {
        if (isLogin && confirmPassword !== "" && password !== "" && confirmPassword !== password) {
            setInfoMessage({message: "Passwords do not match", variant: "warning"});
        }
        else {
            setInfoMessage({message: ""});
        }
    }, [password, confirmPassword])


    const isValidInput = username !== "" && password !== "" && (isLogin || confirmPassword !== "");

    const toggleLogin = () => {
      setIsLogin(!isLogin);
    };

    const handleSignup = async ()  => {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: username, password: password})
        });
        const data = await response.json();
        if (response.ok) {
            setInfoMessage({message: data.message, variant: "success"})
            await handleLogin();
        }
        else {
            setInfoMessage({message: getDetailStringOrDefault(data.detail, "Unknown error"), variant: "warning"})
        }
    };

    const handleLogin = async () => {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch("/api/auth/token", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            setInfoMessage({message: data.message, variant: "success"})

            setUser({id: data.id, name: data.name});
            navigate(`/user/${data.id}/dashboard`)
        }
        else {
            setInfoMessage({message: data.detail, variant: "warning"})
        }
    };

    return (
        <LoginCard isLogin={isLogin}>
                <InputField
                    label="Username:"
                    type="text"
                    value={username}
                    onChange={(e) =>setUsername(e.target.value)}
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
                <div className ="text-center">
                    {infoMessage && <InformationText infoText={infoMessage}/>}
                    <Button
                        variant="primary"
                        label={isLogin ? "Login":"Register"}
                        onClick={isLogin ? handleLogin :handleSignup}
                        disabled={!isValidInput}
                    />
                    <p className="mt-2"> {isLogin ? "No account yet?" : "Already have an account?"} <span className="fw-bold toggle-link" onClick={toggleLogin}>{isLogin ? "Register" : "Login"} here</span></p>
                </div>
            </LoginCard>
    );
}

export default LoginPage;