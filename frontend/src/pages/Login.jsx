import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, API } from '../context/AuthContext.jsx';
import Modal from '../components/Modal.jsx';

const ROLES = [
  { key: 'candidate',    label: 'Candidate' },
  { key: 'interviewer',  label: 'Interviewer' },
  { key: 'company_admin',label: 'Co. Admin' },
  { key: 'global_admin', label: 'Global' },
];

export default function Login() {
  const { login } = useAuth();
  const navigate  = useNavigate();

  const [role,     setRole]     = useState('candidate');
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [error,    setError]    = useState('');
  const [loading,  setLoading]  = useState(false);

  // Register state
  const [showReg,  setShowReg]  = useState(false);
  const [rName,    setRName]    = useState('');
  const [rEmail,   setREmail]   = useState('');
  const [rPass,    setRPass]    = useState('');
  const [rSkills,  setRSkills]  = useState('');

  async function handleLogin() {
    if (!email || !password) { setError('Enter email and password.'); return; }
    setError(''); setLoading(true);
    try {
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);
      form.append('scope', role);
      const res  = await fetch(`${API}/login`, { method: 'POST', body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Login failed');
      login(data.access_token, { email, name: email.split('@')[0] }, role);
      navigate('/dashboard');
    } catch (e) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  async function handleRegister() {
    if (!rName || !rEmail || !rPass) return alert('Fill all fields');
    try {
      const res = await fetch(`${API}/candidates/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: rName, email: rEmail, password: rPass, skills: rSkills, interested_roles: [] }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      alert('Account created! Sign in now.');
      setShowReg(false);
      setEmail(rEmail);
    } catch (e) { alert(e.message); }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'radial-gradient(ellipse at 60% 40%, rgba(59,130,246,0.08) 0%,transparent 65%),var(--bg)' }}>
      <div className="card" style={{ width: 400 }}>
        <div style={{ fontSize: 24, fontWeight: 700, marginBottom: 6 }}>
          Interview<span style={{ color: 'var(--accent)' }}>Manager</span>
        </div>
        <p style={{ color: 'var(--muted)', fontSize: 13, marginBottom: 28 }}>Sign in to your account</p>

        {/* Role picker */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 4, background: 'var(--bg)', padding: 4, borderRadius: 6, marginBottom: 24 }}>
          {ROLES.map(r => (
            <button key={r.key} onClick={() => setRole(r.key)} style={{
              padding: '7px 2px', fontSize: 11, fontWeight: 500,
              border: 'none', borderRadius: 4, cursor: 'pointer',
              fontFamily: 'Inter,sans-serif',
              background: role === r.key ? 'var(--accent)' : 'transparent',
              color: role === r.key ? '#fff' : 'var(--muted)',
            }}>{r.label}</button>
          ))}
        </div>

        {error && <div className="error-box">{error}</div>}

        <div className="form-group">
          <label>Email</label>
          <input type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleLogin()} />
        </div>

        <button className="btn btn-primary btn-block" onClick={handleLogin} disabled={loading}>
          {loading ? 'Signing in…' : 'Sign In'}
        </button>

        <div className="divider" />
        <div style={{ textAlign: 'center', fontSize: 13, color: 'var(--muted)' }}>
          New here?{' '}
          <button className="btn btn-ghost btn-sm" onClick={() => setShowReg(true)}>Create candidate account</button>
        </div>
      </div>

      {/* Register Modal */}
      <Modal open={showReg} onClose={() => setShowReg(false)} title="Create Candidate Account"
        footer={<><button className="btn btn-ghost" onClick={() => setShowReg(false)}>Cancel</button><button className="btn btn-primary" onClick={handleRegister}>Create</button></>}>
        <div className="form-row">
          <div className="form-group"><label>Name</label><input placeholder="Jane Smith" value={rName} onChange={e => setRName(e.target.value)} /></div>
          <div className="form-group"><label>Email</label><input type="email" placeholder="jane@email.com" value={rEmail} onChange={e => setREmail(e.target.value)} /></div>
        </div>
        <div className="form-group"><label>Password</label><input type="password" placeholder="••••••••" value={rPass} onChange={e => setRPass(e.target.value)} /></div>
        <div className="form-group"><label>Skills (optional)</label><input placeholder="Python, React…" value={rSkills} onChange={e => setRSkills(e.target.value)} /></div>
      </Modal>
    </div>
  );
}
