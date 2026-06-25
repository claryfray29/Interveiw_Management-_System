import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';

export default function Interviews() {
  const { token } = useAuth();
  const [interviews, setInterviews] = useState([]);
  const [loading,    setLoading]    = useState(true);
  const [selected,   setSelected]   = useState(null);
  const [feedback,   setFeedback]   = useState('');

  async function load() {
    setLoading(true);
    try { setInterviews(await apiFetch('/interviews/upcoming', token)); } catch (e) {}
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function submitFeedback() {
    if (!feedback) { alert('Enter feedback'); return; }
    try {
      await apiFetch(`/interviews/${selected}/feedback?feedback=${encodeURIComponent(feedback)}`, token, { method: 'POST' });
      setSelected(null); setFeedback('');
      load();
    } catch (e) { alert(e.message); }
  }

  if (loading) return <Spinner />;

  return (
    <div>
      <div className="page-header">
        <div><h1>Upcoming Interviews</h1><p>Your scheduled sessions</p></div>
        <button className="btn btn-ghost btn-sm" onClick={load}>↻ Refresh</button>
      </div>

      {interviews.length === 0 ? (
        <div className="empty">
          <div className="title">No upcoming interviews</div>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Candidate</th><th>Application</th><th>Scheduled</th><th>Status</th><th>Feedback</th><th></th></tr></thead>
            <tbody>
              {interviews.map(i => (
                <tr key={i.id}>
                  <td>#{i.id}</td>
                  <td>{i.candidate_id}</td>
                  <td>#{i.application_id}</td>
                  <td>{new Date(i.scheduled_time).toLocaleString()}</td>
                  <td><span className={`badge badge-${i.status}`}>{i.status}</span></td>
                  <td className="table-cell-truncated">{i.feedback || '—'}</td>
                  <td><button className="btn btn-ghost btn-sm" onClick={() => { setSelected(i.id); setFeedback(''); }}>+ Feedback</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal open={!!selected} onClose={() => setSelected(null)} title="Post Feedback"
        footer={<><button className="btn btn-ghost" onClick={() => setSelected(null)}>Cancel</button><button className="btn btn-primary" onClick={submitFeedback}>Post</button></>}>
        <div className="form-group"><label>Feedback</label><textarea placeholder="Candidate showed strong problem-solving skills…" value={feedback} onChange={e => setFeedback(e.target.value)} /></div>
      </Modal>
    </div>
  );
}