import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user,  setUser]  = useState(null);
  const [role,  setRole]  = useState(null);

  const login  = (tok, usr, rl) => { setToken(tok); setUser(usr); setRole(rl); };
  const logout = () => { setToken(null); setUser(null); setRole(null); };

  return (
    <AuthContext.Provider value={{ token, user, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

export const API = 'http://localhost:8000';

export async function apiLogin(email, password) {
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}

export async function apiFetch(path, token, options = {}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  // 204 No Content or empty body — treat as success with no data
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};

  if (!res.ok) {
    // data.detail may itself be an object (FastAPI validation errors are arrays)
    // — always coerce to a string so the UI never shows [object Object]
    const detail = data.detail;
    if (Array.isArray(detail)) {
      throw new Error(detail.map(e => e.msg || JSON.stringify(e)).join('; '));
    }
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail) || `Error ${res.status}`);
  }

  return data;
}