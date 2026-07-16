import { useEffect, useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import api from "../api";
import {useAuth} from "../AuthContext";

export default function Dashboard() {
    const {user} = useAuth();
    const [error, setError] = useState("");
    const [stats, setStats] = useState(null);
    
    useEffect(() => {
        api.get("/users/me/dashboard").then((resp) => setStats(resp.data)).catch(() => setError("Couldn't set dashboard."))

    }, []);

    return (
        <div>
            <div className="hero">
                <h1>Welcome back, {user?.username}</h1>
                <p>Every bug you fix sharpens your skillset. Good luck</p>
            </div>
            {error && <div className="error-banner">{error}</div>}
            {stats && (
                <>
                <div className="stats-row">
        
                </div>

                <div className="section-title">Achievements</div>
                </>

            )}

        </div>
    );
}