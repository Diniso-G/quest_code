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
                <p>{challenge.description}</p>
            </div>

            {error && <div className="error-banner">{error}</div>}

            <div className="section-title">Evidence (the buggy code)</div>
            <div className="code-block"> {challenge.buggy_code}</div>

            {!result && (
                <>
                    <div className="section-title">Hints ({hintsUsed}/3 used - using hints reduces XP earned)</div>
                    {hints.map((h, i) => (
                        <div key={i} className="case-card">
                            <div className="case-id">HINT {i + 1}</div>
                            <p>{h}</p>
                        </div>
                    ))}
                    {hints.length < 3 && (
                        <button className="btn" onClick={revealNextHint}>Reveal Hint {hints.length + 1}</button>
                    )}

                    <div className="section-title">Your fix</div>
                    <form onSubmit={handleSubmit}>
                        <div className="field">
                            <textarea rows={10} value={answer} onChange={(e) => setAnswer(e.target.value)} 
                                placeholder="Paste the corrected code, or explain the bug and how you'd fix it..."
                                required />
                        </div>
                        <button className="btn btn-primary" disabled={submitting}>
                            {submitting ? "Reviewing..." : "Submit fix"}
                        </button>
                    </form>
                </>
            )}

            {result && (
                <div className="case-card">
                    <div className="case-id">VERDICT</div>
                    <div className="case-title">
                        {result.is_correct ? "Case closed - bug fixed" : "Not quite - case still open"}
                    </div>
                    <p>Score: {result.ai_score}/100</p>
                    <p>{result.ai_feedback}</p>

                    {result.xp_awarded > 0 && (
                        <p>+{result.xp_awarded} XP - Level {result.new_level} - FRE {result.new_streak} day streak</p>

                    )}

                    {result.achievements_unlocked.length > 0 && (
                        <div>
                            {result.achievements_unlocked.map((a) => (
                                <span key={a} className="achievement-chip"> Troph NEW: {a}</span>
                            ))}
                        </div>
                    )}

                    <div className="section-title"> Correct solution</div>
                    <div className="code-block">{result.correct_solution}</div>

                    <div className="section-title"> Explanation</div>
                    <p>{result.explanation}</p>

                    <Link to="/challenges" className="btn btn-primary">
                    Find another case -</Link>
                </div>
            )}
        </div>
    )
}
