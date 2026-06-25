import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';

export default function Jobs() {
  const { token } = useAuth();
  const [jobs,    setJobs]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [job,     setJob]     = useState(null);   // selected job for apply
  const [resume,  setResume]  = useState('');
  const [msg,     setMsg]     = useState('');

  async function load() {
    setLoading(true);
    try { setJobs(await apiFetch('/jobs/available', token)); } catch (e) {}
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function apply() {
    if (!resume) { setMsg('Enter resume URL'); return; }
    try {
      await apiFetch('/applications/', token, { method: 'POST', body: JSON.stringify({ job_id: job.id, resume }) });
      setMsg(''); setJob(null); setResume('');
      alert('Application submitted!');
    } catch (e) { setMsg(e.message); }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>Available Jobs</h1><p>Jobs matching your profile</p></div>
        <button className="btn btn-ghost btn-sm" onClick={load}>↻ Refresh</button>
      </div>

      {jobs.length === 0 ? (
        <div className="empty">
          <div className="title">No jobs available</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Title</th><th>Description</th><th>Vacancies</th><th>Skills</th><th></th></tr></thead>
            <tbody>
              {jobs.map(j => (
                <tr key={j.id}>
                  <td><strong>{j.title}</strong></td>
                  <td className="table-cell-description">{j.description}</td>
                  <td>{j.vacancies}</td>
                  <td>{(j.skills_required || '').split(',').map((s, i) => <span key={i} className="chip">{s.trim()}</span>)}</td>
                  <td><button className="btn btn-success btn-sm" onClick={() => { setJob(j); setResume(''); setMsg(''); }}>Apply</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal open={!!job} onClose={() => setJob(null)} title={`Apply — ${job?.title}`}
        footer={<><button className="btn btn-ghost" onClick={() => setJob(null)}>Cancel</button><button className="btn btn-primary" onClick={apply}>Submit</button></>}>
        {msg && <div className="error-box">{msg}</div>}
        <div className="form-group"><label>Resume URL</label><input placeholder="https://…" value={resume} onChange={e => setResume(e.target.value)} /></div>
      </Modal>
    </div>
  );
}