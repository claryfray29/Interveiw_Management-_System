import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';

export default function MyApplications() {
  const { token } = useAuth();
  const [apps,    setApps]    = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setApps(await apiFetch('/applications/status', token)); } catch (e) {}
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function withdraw(id) {
    if (!window.confirm('Withdraw this application?')) return;
    try {
      await apiFetch(`/applications/${id}`, token, { method: 'DELETE' });
      load();
    } catch (e) { alert(e.message); }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>My Applications</h1><p>Track your application statuses</p></div>
        <button className="btn btn-ghost btn-sm" onClick={load}>↻ Refresh</button>
      </div>

      {apps.length === 0 ? (
        <div className="empty">
          <div className="title">No applications yet</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Job ID</th><th>Status</th><th>Resume</th><th></th></tr></thead>
            <tbody>
              {apps.map(a => (
                <tr key={a.id}>
                  <td>#{a.id}</td>
                  <td>{a.job_id}</td>
                  <td><span className={`badge badge-${a.status}`}>{a.status}</span></td>
                  <td><a href={a.resume} target="_blank" rel="noreferrer" className="table-link">View ↗</a></td>
                  <td><button className="btn btn-danger btn-sm" onClick={() => withdraw(a.id)}>Withdraw</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}