import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';

export default function CompanyJobs() {
  const { token } = useAuth();
  const [jobs,      setJobs]      = useState([]);
  const [loading,   setLoading]   = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form,      setForm]      = useState({ title: '', description: '', role_id: '', vacancies: '', skills_required: '' });

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  async function load() {
    setLoading(true);
    try { setJobs(await apiFetch('/jobs/available', token)); } catch (e) {}
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function addJob() {
    const { title, description, role_id, vacancies, skills_required } = form;
    if (!title || !description || !role_id || !vacancies || !skills_required) { alert('Fill all fields'); return; }
    try {
      await apiFetch('/jobs/', token, { method: 'POST', body: JSON.stringify({ title, description, role_id: +role_id, vacancies: +vacancies, skills_required }) });
      setShowModal(false);
      setForm({ title: '', description: '', role_id: '', vacancies: '', skills_required: '' });
      load();
    } catch (e) { alert(e.message); }
  }

  async function deleteJob(id) {
    if (!window.confirm('Delete this job?')) return;
    try { await apiFetch(`/jobs/${id}`, token, { method: 'DELETE' }); load(); }
    catch (e) { alert(e.message); }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>Job Listings</h1><p>Manage open positions</p></div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Post Job</button>
      </div>

      {jobs.length === 0 ? (
        <div className="empty"><div className="icon">💼</div><div className="title">No jobs posted yet</div></div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Title</th><th>Vacancies</th><th>Skills</th><th></th></tr></thead>
            <tbody>
              {jobs.map(j => (
                <tr key={j.id}>
                  <td>#{j.id}</td>
                  <td><strong>{j.title}</strong></td>
                  <td>{j.vacancies}</td>
                  <td>{(j.skills_required || '').split(',').slice(0,3).map((s, i) => <span key={i} className="chip">{s.trim()}</span>)}</td>
                  <td><button className="btn btn-danger btn-sm" onClick={() => deleteJob(j.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Post Job"
        footer={<><button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button><button className="btn btn-primary" onClick={addJob}>Post</button></>}>
        <div className="form-group"><label>Title</label><input placeholder="Backend Engineer" value={form.title} onChange={set('title')} /></div>
        <div className="form-group"><label>Description</label><textarea placeholder="Role description…" value={form.description} onChange={set('description')} /></div>
        <div className="form-row">
          <div className="form-group"><label>Role ID</label><input type="number" placeholder="1" value={form.role_id} onChange={set('role_id')} /></div>
          <div className="form-group"><label>Vacancies</label><input type="number" placeholder="3" value={form.vacancies} onChange={set('vacancies')} /></div>
        </div>
        <div className="form-group"><label>Skills Required</label><input placeholder="Python, Docker…" value={form.skills_required} onChange={set('skills_required')} /></div>
      </Modal>
    </div>
  );
}
