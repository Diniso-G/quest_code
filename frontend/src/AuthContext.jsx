import { createContext, useContext, useState, useEffect, useCallback } from "react";
import api from "./api";

const AuthContext = createContext(null);

export function AuthProvider({children}) {
    const [token, setToken] = useState(() => localStorage.getItem("cq_token"));
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const refreshUser = useCallback(async () => {
        if (!localStorage.getItem("cq_token")) {
            setUser(null);
            setLoading(false);
            return;
        }
        try {
            const resp = await api.get("/user/me");
            setUser(resp.data);
        }
        catch {
            logout();
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        refreshUser() }, [refreshUser]);

    function login(newToken) {
        localStorage.setItem("cq_token", newToken);
        setToken(newToken);
        refreshUser();
    }

    function logout() {
        localStorage.removeItem("cq_token");
        setToken(null);
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ token, user, loading, login, logout, refreshUser}}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}