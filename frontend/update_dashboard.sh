```bash
#!/bin/bash

# Navigate straight to the source path
cd ~/Projects/Interveiw_Management-_System/frontend

# Overwrite the frozen file on the storage disk completely
cat << 'EOF' > src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { useAuth, apiFetch } from '../context/AuthContext.jsx';

export default function Dashboard() {
  const { token, role, user } = useAuth();
  const [stats, setStats] = useState({});

  useEffect(() => {
    if (role === 'candidate') {
      apiFetch('/jobs/available', token).then(d => setStats(s => ({ ...s, jobs: d.length }))).catch(() => {});
      apiFetch('/applications/status', token).then(d => setStats(s => ({ ...s, apps: d.length }))).catch(() => {});
    }
    if (role === 'interviewer') {
      apiFetch('/interviews/upcoming', token).then(d => setStats(s => ({ ...s, interviews: d.length }))).catch(() => {});
    }
    if (role === 'company_admin') {
      apiFetch('/companies/applications', token).then(d => setStats(s => ({ ...s, apps: d.length }))).catch(() => {});
    }
  }, [role, token]);

  const hints = {
    candidate:    'Browse available jobs and track your applications from the sidebar.',
    interviewer:  'Check your upcoming interviews and post feedback after sessions.',
    company_admin: 'Manage applications, job listings, and your team from the sidebar.',
    global_admin:  'Add and manage companies from the sidebar.',
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Welcome back, {user?.name}</p>
        </div>
      </div>

      <div className="stats-grid">
        {role === 'candidate' && <>
          <div className="stat-card"><div className="label">Available Jobs</div><div className="value">{stats.jobs ?? '…'}</div></div>
          <div className="stat-card"><div className="label">My Applications</div><div className="value">{stats.apps ?? '…'}</div></div>
        </>}
        {role === 'interviewer' &&
          <div className="stat-card"><div className="label">Upcoming Interviews</div><div className="value">{stats.interviews ?? '…'}</div></div>
        }
        {role === 'company_admin' &&
          <div className="stat-card"><div className="label">Applications</div><div className="value">{stats.apps ?? '…'}</div></div>
        }
        {role === 'global_admin' &&
          <div className="stat-card"><div className="label">Platform</div><div className="value">Admin</div></div>
        }
      </div>

      <p style={{ color: 'var(--muted)', fontSize: 13 }}>{hints[role]}</p>
    </div>
  );
}
EOF

echo "Dashboard component modified successfully!"
