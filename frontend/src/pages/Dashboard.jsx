import { useEffect, useState } from "react";
import {Link, useNavigate} from "react-router-dom";
import api from "../api";
import {useAuth} from "../AuthContext";

export default function Dashboard() {
    const {user} = useAuth();
    const [error, setError] = useState("");
    const [stats, setStats] = useState(null);

    const [history, setHistory] = useState(null);
    const [showHistory, setShowHistory] = useState(false);
    const [historyError, setHistoryError] = useState("");
    const [loadingHistory, setLoadingHistory] = useState(false);

    
    useEffect(() => {
        api.get("/users/me/dashboard").then((resp) => setStats(resp.data)).catch(() => setError("Couldn't load your case file. Try refreashing."))
    }, []);

    const xpPcct = stats ? Math.round(((100 - stats.xp_to_next_level) / 100) * 100): 0;

    const toggleHistory = () => {
        const next = !showHistory;
        setShowHistory(next);
        if (next && history == null) {
            setLoadingHistory(true);
            api.get("/users/me/history")
                .then((resp) => setHistory(resp.data))
                .catch(() => setHistoryError("Couldn't load your case history. Try refreashing browser."))
                .finally(() => setLoadingHistory(false));
        }
    };

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
                    <div className="stat-box">
                        <div className="num">{stats.level}</div>
                        <div className="label">Level</div>
                        <div className="xp-bar"><div className="xp-bar-fill" style={{width: `${xpPcct}%`}}/></div>
                    </div>
                    <div className="stat-box">
                        <div className="num">{stats.xp}</div>
                        <div className="label">Total XP</div>
                    </div>
                    <div className="stat-box">
                        <div className="num">{stats.bugs_fixed}</div>
                        <div className="label">Bugs Fixed</div>
                    </div>
                    <div className="stat-box">
                        <div className="num">{stats.streak}</div>
                        <div className="label">Day Streak</div>
                    </div>
        
                </div>

                <div className="section-title">Achievements</div>
                {stats.achievements.length === 0 ? (<p> No badges yet- solve your first case to earn one.</p>
                ) : (
                    <div>
                        {stats.achievements.map((a) => (<span key={a} className="achievement-chip"> Crwn {a}</span>
                    ))}
                    </div>
                )}
                </>

            )}

            <div className="section-title history-title">Case History
                <button className="btn btn-primary" onClick={toggleHistory}>
                    {showHistory ? "Hide history" : "View History"}
                </button>
            </div>

            {showHistory && (
                <div className="history-list">
                    {loadingHistory && <p className="loading-dot">Loading...</p>}
                    {loadingHistory && <div className="error-banner">{historyError}</div>}
                    {!loadingHistory && history && history.length === 0 && (
                        <p>No activity yet - go complete something!</p>
                    )}
                    {!loadingHistory && history && history.length > 0 && (
                        <div className="card-grid">
                            {history.map((item) => (
                                <div key={item.submission_id} className="history-row">
                                    <div className="history-main">
                                        <span className="case-title">{item.challenge_id}</span>
                                        <span className={`tag difficulty- ${item.difficulty}`}>{item.difficulty}</span>
                                    </div>
                                    <div className="history-main">
                                        <span className={item.is_correct ? "history-status ok" : "history-status fail"}>
                                            {item.is_correct ? "Solved" : "Attempted"}
                                        </span>
                                        <span>+{item.xp_awarded}</span>
                                        <span>{new Date(item.created_at).toLocaleDateString()}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
                )}

            <div className="section-title">Ready for the next case?</div>
            <Link to="/challenges" className="btn btn-primary">Open Case Files</Link>
         </div>
    );
}