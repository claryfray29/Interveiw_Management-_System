import React, { useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';

export default function Profile() {
  const { token } = useAuth();
  const [skills, setSkills] = useState('');
  const [resume, setResume] = useState('');
  const [msg,    setMsg]    = useState('');

  async function save() {
    if (!skills || !resume) { setMsg('Fill both fields.'); return; }
    try {
      await apiFetch(`/candidates/profile?skills=${encodeURIComponent(skills)}&resume=${encodeURIComponent(resume)}`, token, { method: 'PUT' });
      setMsg('✓ Profile saved!');
    } catch (e) { setMsg(e.message); }
  }

  return (
    <div>
      <div className="page-header"><div><h1>My Profile</h1><p>Update your skills and resume</p></div></div>
      <div className="card" style={{ maxWidth: 500 }}>
        {msg && <div className={msg.startsWith('✓') ? '' : 'error-box'} style={msg.startsWith('✓') ? { color: 'var(--success)', fontSize: 13, marginBottom: 14 } : {}}>{msg}</div>}
        <div className="form-group"><label>Skills (comma-separated)</label><input placeholder="Python, React, SQL…" value={skills} onChange={e => setSkills(e.target.value)} /></div>
        <div className="form-group"><label>Resume URL</label><input placeholder="https://drive.google.com/…" value={resume} onChange={e => setResume(e.target.value)} /></div>
        <button className="btn btn-primary" onClick={save}>Save Changes</button>
      </div>
    </div>
  );
}
