import React, { useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Modal from '../components/Modal.jsx';

export default function Companies() {
  const { token } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [added,     setAdded]     = useState([]);
  const [form, setForm] = useState({ company_name: '', super_admin_name: '', super_admin_email: '', super_admin_password: '' });

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  async function addCompany() {
    if (!form.company_name || !form.super_admin_name || !form.super_admin_email || !form.super_admin_password) { alert('Fill all fields'); return; }
    try {
      await apiFetch('/companies/', token, { method: 'POST', body: JSON.stringify(form) });
      setAdded(a => [...a, form.company_name]);
      alert(`Company "${form.company_name}" added!`);
      setShowModal(false);
      setForm({ company_name: '', super_admin_name: '', super_admin_email: '', super_admin_password: '' });
    } catch (e) { alert(e.message); }
  }

  return (
    <div>
      <div className="page-header">
        <div><h1>Companies</h1><p>Onboard new organisations</p></div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Company</button>
      </div>

      {added.length === 0 ? (
        <div className="empty">
          <div className="title">No companies added this session</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Company</th></tr></thead>
            <tbody>{added.map((c, i) => <tr key={i}><td>{c}</td></tr>)}</tbody>
          </table>
        </div>
      )}

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Add Company & Super Admin"
        footer={<><button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button><button className="btn btn-primary" onClick={addCompany}>Add</button></>}>
        <div className="form-group"><label>Company Name</label><input placeholder="Acme Corp" value={form.company_name} onChange={set('company_name')} /></div>
        <div className="divider" />
        <div className="form-group"><label>Super Admin Name</label><input placeholder="John Doe" value={form.super_admin_name} onChange={set('super_admin_name')} /></div>
        <div className="form-group"><label>Super Admin Email</label><input type="email" placeholder="admin@acme.com" value={form.super_admin_email} onChange={set('super_admin_email')} /></div>
        <div className="form-group"><label>Super Admin Password</label><input type="password" placeholder="••••••••" value={form.super_admin_password} onChange={set('super_admin_password')} /></div>
      </Modal>
    </div>
  );
}