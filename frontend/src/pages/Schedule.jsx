import React, { useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';

export default function Schedule() {
  const { token } = useAuth();
  const [form, setForm] = useState({ appId: '', interviewerId: '', start: '', end: '' });
  const [msg,  setMsg]  = useState('');

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  async function schedule() {
    if (!form.appId || !form.interviewerId || !form.start || !form.end) { setMsg('Fill all fields'); return; }
    try {
      await apiFetch('/interviews/', token, {
        method: 'POST',
        body: JSON.stringify({ application_id: +form.appId, interviewer_id: +form.interviewerId, scheduled_start: form.start, scheduled_end: form.end, status: 'scheduled' }),
      });
      setMsg('Interview scheduled! Calendar invites sent successfully.');
      setForm({ appId: '', interviewerId: '', start: '', end: '' });
    } catch (e) { setMsg(e.message); }
  }

  return (
    <div>
      <div className="page-header"><div><h1>Schedule Interview</h1><p>Calendar invites are sent automatically</p></div></div>
      <div className="card schedule-card-constrained">
        {msg && (
          <div className={msg.includes('successfully') ? 'success-message-text' : 'error-box'}>
            {msg}
          </div>
        )}
        <div className="form-group"><label>Application ID</label><input type="number" placeholder="e.g. 42" value={form.appId} onChange={set('appId')} /></div>
        <div className="form-group"><label>Interviewer ID</label><input type="number" placeholder="e.g. 7" value={form.interviewerId} onChange={set('interviewerId')} /></div>
        <div className="form-row">
          <div className="form-group"><label>Start</label><input type="datetime-local" value={form.start} onChange={set('start')} /></div>
          <div className="form-group"><label>End</label><input type="datetime-local" value={form.end} onChange={set('end')} /></div>
        </div>
        <button className="btn btn-primary" onClick={schedule}>Schedule</button>
      </div>
    </div>
  );
}