import React, { useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Modal from '../components/Modal.jsx';

export default function Team() {
  const { token } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', password: '', account_type: 'interviewer', role_id: '' });

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  async function addUser() {
    if (!form.name || !form.email || !form.password) { alert('Fill all fields'); return; }
    const payload = { name: form.name, email: form.email, password: form.password, account_type: form.account_type };
    if (form.account_type === 'interviewer' && form.role_id) payload.role_id = +form.role_id;
    try {
      await apiFetch('/companies/users', token, { method: 'POST', body: JSON.stringify(payload) });
      alert('User added!');
      setShowModal(false);
      setForm({ name: '', email: '', password: '', account_type: 'interviewer', role_id: '' });
    } catch (e) { alert(e.message); }
  }

  return (
    <div>
      <div className="page-header">
        <div><h1>Team</h1><p>Add interviewers and admins</p></div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add User</button>
      </div>
      <p style={{ color: 'var(--muted)', fontSize: 13 }}>💡 Super admins can add company admins. All admins can add interviewers.</p>

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Add Team Member"
        footer={<><button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button><button className="btn btn-primary" onClick={addUser}>Add</button></>}>
        <div className="form-group"><label>Name</label><input placeholder="Full name" value={form.name} onChange={set('name')} /></div>
        <div className="form-group"><label>Email</label><input type="email" placeholder="user@company.com" value={form.email} onChange={set('email')} /></div>
        <div className="form-group"><label>Password</label><input type="password" placeholder="••••••••" value={form.password} onChange={set('password')} /></div>
        <div className="form-group">
          <label>Account Type</label>
          <select value={form.account_type} onChange={set('account_type')}>
            <option value="interviewer">Interviewer</option>
            <option value="company_admin">Company Admin</option>
          </select>
        </div>
        {form.account_type === 'interviewer' && (
          <div className="form-group"><label>Role ID</label><input type="number" placeholder="e.g. 1" value={form.role_id} onChange={set('role_id')} /></div>
        )}
      </Modal>
    </div>
  );
}
