import InputField from "../components/InputField.tsx";
import Button from "../components/Button.tsx";
import LoginCard from "../components/LoginCard.tsx";
import {useContext, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {useNavigate} from "react-router-dom";

function LoginPage() {

    const navigate = useNavigate()

    const [isLogin, setIsLogin] = useState(true);

    const toggleLogin = () => {
      setIsLogin(!isLogin);
    };

    const [isValidInput, setIsValidInput] = useState(false);

    const [errorMessage, setErrorMessage] = useState("");
    const { setUser } = useContext(AuthContext)!;


    const handleSignup = async ()  => {
        const response = await fetch("/api/auth/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: username, password: password})
        });
        const data = await response.json();
        setErrorMessage(data.message)
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

        if (response.ok) {
            const data = await response.json();
            setErrorMessage(data.message)

            setUser({id: data.id, name: data.name});
            navigate(`/user/${data.id}/dashboard`)
        }


    };

    const validatePasswords = () => {
        validateInput()
        if (password !== confirmPassword) {
            setErrorMessage(("Passwords do not match."));
        }
        else {
            setErrorMessage("");
        }
    }

    const validateInput = () => {
        if (username === "" ||
            password === "" ||
            (!isLogin && (confirmPassword === "" || confirmPassword !== password))){
            setIsValidInput(false)
        }
        else {
            setIsValidInput(true)
        }
    }

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    return (
        <LoginCard isLogin={isLogin}>
                <InputField
                    label="Username:"
                    type="text"
                    value={username}
                    onChange={(e) =>setUsername(e.target.value)}
                    onBlur={validateInput}
                />
                <InputField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onBlur={validateInput}
                />
                {!isLogin && <InputField
                    label="Confirm Password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    onBlur={validatePasswords}
                />}
                <div className ="text-center">
                    {errorMessage && <p className="text-warning">{errorMessage}</p>}
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