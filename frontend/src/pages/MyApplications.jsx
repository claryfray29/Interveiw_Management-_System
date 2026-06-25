import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';

export default function MyApplications() {
  const { token } = useAuth();
  const [apps,        setApps]        = useState([]);
  const [loading,     setLoading]     = useState(true);
  const [confirmId,   setConfirmId]   = useState(null); // id pending withdrawal confirm
  const [withdrawing, setWithdrawing] = useState(null); // id currently being withdrawn
  const [error,       setError]       = useState('');

  async function load() {
    setLoading(true);
    setError('');
    try { setApps(await apiFetch('/applications/status', token)); }
    catch (e) { setError(e.message); }
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function withdraw(id) {
    setWithdrawing(id);
    setConfirmId(null);
    setError('');
    try {
      await apiFetch(`/applications/${id}`, token, { method: 'DELETE' });
      setApps(prev => prev.filter(a => a.id !== id));
    } catch (e) {
      setError(e.message);
    } finally {
      setWithdrawing(null);
    }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>My Applications</h1><p>Track your application statuses</p></div>
        <button className="btn btn-ghost btn-sm" onClick={load}>↻ Refresh</button>
      </div>

      {error && <div className="error-box" style={{ marginBottom: 16 }}>{error}</div>}

      {apps.length === 0 ? (
        <div className="empty">
          <div className="icon">📋</div>
          <div className="title">No applications yet</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Job ID</th><th>Status</th><th>Resume</th><th></th></tr>
            </thead>
            <tbody>
              {apps.map(a => (
                <tr key={a.id}>
                  <td>#{a.id}</td>
                  <td>{a.job_id}</td>
                  <td><span className={`badge badge-${a.status}`}>{a.status}</span></td>
                  <td><a href={a.resume} target="_blank" rel="noreferrer" className="table-link">View ↗</a></td>
                  <td style={{ textAlign: 'right' }}>
                    {confirmId === a.id ? (
                      <span style={{ display: 'inline-flex', gap: 6, alignItems: 'center' }}>
                        <span style={{ fontSize: 12, color: 'var(--muted)' }}>Sure?</span>
                        <button
                          className="btn btn-danger btn-sm"
                          disabled={withdrawing === a.id}
                          onClick={() => withdraw(a.id)}
                        >
                          {withdrawing === a.id ? '…' : 'Yes, withdraw'}
                        </button>
                        <button className="btn btn-ghost btn-sm" onClick={() => setConfirmId(null)}>
                          Cancel
                        </button>
                      </span>
                    ) : (
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => setConfirmId(a.id)}
                      >
                        Withdraw
                      </button>
                    )}
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