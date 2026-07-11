import { useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import {useAuth} from "../AuthContext";

export default function Registration() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div className="auth-card">
            <form onSubmit={handleSubmit}>
                <div className="field">
                    <label>Email</label>
                    <input type="email" value={email} onChange={}/>
                </div>    
                <div className="field">
                    <label>Password</label>
                    <input type="password" value={email} onChange={}/>
                </div> 
                <button className="btn btn-primary">
                    
                </button>
            </form>         
        </div>
    )
}