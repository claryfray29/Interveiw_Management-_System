import React, { useState, useEffect } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Modal from '../components/Modal.jsx';

export default function Companies() {
  const { token } = useAuth();
  const [showModal, setShowModal] = useState(false);
  
  // 1. Change this to track the full list of companies fetched from MySQL
  const [companies, setCompanies] = useState([]);
  const [form, setForm] = useState({ company_name: '', super_admin_name: '', super_admin_email: '', super_admin_password: '' });

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  // 2. Fetch the existing company rows from the backend the moment the page mounts
  const fetchCompanies = async () => {
    try {
      const data = await apiFetch('/companies/', token);
      if (Array.isArray(data)) {
        setCompanies(data);
      }
    } catch (e) {
      console.error("Failed to load companies:", e.message);
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, [token]);

  async function addCompany() {
    if (!form.company_name || !form.super_admin_name || !form.super_admin_email || !form.super_admin_password) { alert('Fill all fields'); return; }
    try {
      await apiFetch('/companies/', token, { method: 'POST', body: JSON.stringify(form) });
      alert(`Company "${form.company_name}" added!`);
      setShowModal(false);
      setForm({ company_name: '', super_admin_name: '', super_admin_email: '', super_admin_password: '' });
      
      // 3. Re-fetch from the database right after adding to pull the newly persistent data row
      fetchCompanies();
    } catch (e) { alert(e.message); }
  }

  return (
    <div>
      <div className="page-header">
        <div><h1>Companies</h1><p>Onboard new organisations</p></div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Company</button>
      </div>

      {/* 4. Render the database records instead of the old transient session array */}
      {companies.length === 0 ? (
        <div className="empty">
          <div className="title">No companies found in database</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Company Name</th></tr></thead>
            <tbody>
              {companies.map((c, i) => (
                <tr key={c.id || i}>
                  {/* Access the name field returned from your backend schemas/models */}
                  <td>{c.name || c.company_name}</td>
                </tr>
              ))}
            </tbody>
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