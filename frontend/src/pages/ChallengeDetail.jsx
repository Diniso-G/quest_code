import { useEffect, useState } from "react";
import { Link, useParams} from "react-router-dom";
import api from "../api";
import { useAuth } from "../AuthContext";

export default function ChallengeDetail(){
    const { id } = useParams();
    const { refreshUser } = useAuth();
    const [challenge, setChallenge] = useState(null);
    const [answer, setAnswer] = useState("");
    const [hints, setHints] = useState([]);
    const [hintsUsed, setHintsUsed] = useState(0);
    const [result, setResult] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        setChallenge(null)
        setAnswer("")
        setHints([])
        setHintsUsed(0)
        setResult(null)
        setError("")
        api.get(`/challenges/${id}`).then((resp) => setChallenge(resp.data)).catch(() => setError("Case not found."))
    }, [id]);

    async function revealNextHint() {
        const nextHintNumber = hints.length + 1;
        if (nextHintNumber > 3) return;
        try {
            const resp = await api.get(`/challenges/${id}/hint/${nextHintNumber}`);
            setHints([...hints, resp.data.hint_text]);
            setHintsUsed(nextHintNumber);
        }
        catch {
            setError("Couldn't fetch a hint right now.");
        }
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setSubmitting(true);
        setError("");
        try {
            const resp = await api.post(`/submissions`, { challenge_id: Number(id), user_answer: answer}, {params: { hints_used: hintsUsed} });
            setResult(resp.data);
            refreshUser();
        }
        catch (err) {
            setError(err.response?.data?.detail || "Couldn't submit your fix.");
        }
        finally {
            setSubmitting(false);
        }
    }
    
    if (error && !challenge) return <div className="error-banner">{error}</div>
    if (!challenge) return <p className="loading-dot">Loading case</p>

    return (
        <div>
            <Link to="/challenges">-Back to case files</Link>
            <div className="hero">
                <div className="case-id">CASE-{String(challenge.id).padStart(4, "0")} - {challenge.language}</div>
                <h1>{challenge.title}</h1>
                <span className={`tag difficulty-${challenge.difficulty}`}>{challenge.difficulty}</span>
            </div>
        </div>


    )

}
