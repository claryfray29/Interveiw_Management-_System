import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';

const STATUSES = ['applied', 'shortlisted', 'rejected', 'hired'];

export default function CompanyApplications() {
  const { token } = useAuth();
  const [apps,    setApps]    = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setApps(await apiFetch('/companies/applications', token)); } catch (e) {}
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function updateStatus(id, status) {
    try {
      await apiFetch(`/applications/${id}/status?status=${encodeURIComponent(status)}`, token, { method: 'PUT' });
      load();
    } catch (e) { alert(e.message); }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>Applications</h1><p>Review incoming applications</p></div>
        <button className="btn btn-ghost btn-sm" onClick={load}>↻ Refresh</button>
      </div>

      {apps.length === 0 ? (
        <div className="empty">
          <div className="title">No applications yet</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Candidate</th><th>Job</th><th>Status</th><th>Resume</th><th>Update</th></tr></thead>
            <tbody>
              {apps.map(a => (
                <tr key={a.id}>
                  <td>#{a.id}</td>
                  <td>{a.candidate_id}</td>
                  <td>{a.job_id}</td>
                  <td><span className={`badge badge-${a.status}`}>{a.status}</span></td>
                  <td><a href={a.resume} target="_blank" rel="noreferrer" className="table-link">View</a></td>
                  <td>
                    <select className="inline" defaultValue="" onChange={e => e.target.value && updateStatus(a.id, e.target.value)}>
                      <option value="">— change —</option>
                      {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}