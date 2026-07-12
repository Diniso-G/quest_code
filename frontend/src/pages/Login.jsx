import { useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import api from "../api";
import {useAuth} from "../AuthContext";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);
    const {login} = useAuth();
    const navigate = useNavigate();


    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setBusy(true);

        try {
            const form = new URLSearchParams();
            form.append("username", email);
            form.append("password", password);
            const resp = await api.post("/auth/login", form);
            login(resp.data.access_token);
            navigate("/dashboard");
        } catch (err) {
            setError(err.response?.data?.detail || "Login Failed");
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="auth-card">
            <h2> Welcome back</h2>
            <p> Sign in to pick up where your last case left off </p>
            {error && <div className="error-banner"> {error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="field">
                    <label>Email</label>
                    <input type="email" value={email}/>
                </div>    
                <div className="field">
                    <label>Password</label>
                    <input type="password" value={email}/>
                </div> 
                <button className="btn btn-primary">
                    {busy ? "Signing in...": "Sign in"}
                </button>
            </form>         
            <p>No account? <Link to="/register">Create an Account</Link>
            </p>
        </div>
    );
}

