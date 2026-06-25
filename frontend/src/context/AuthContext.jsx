import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user,  setUser]  = useState(null);  // { email, name }
  const [role,  setRole]  = useState(null);  // candidate | interviewer | company_admin | global_admin

  const login  = (tok, usr, rl) => { setToken(tok); setUser(usr); setRole(rl); };
  const logout = () => { setToken(null); setUser(null); setRole(null); };

  return (
    <AuthContext.Provider value={{ token, user, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

// Base URL — change if your backend runs elsewhere
export const API = 'http://localhost:8000';

// Helper: authenticated JSON fetch
export async function apiFetch(path, token, options = {}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}
