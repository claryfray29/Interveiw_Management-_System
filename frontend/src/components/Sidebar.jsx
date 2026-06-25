import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

const NAV_MENU = {
  candidate: [
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'My Profile', to: '/profile' },
    { label: 'Jobs', to: '/jobs' },
    { label: 'My Applications', to: '/applications' }
  ],
  interviewer: [
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'Interviews', to: '/interviews' }
  ],
  company_admin: [
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'Manage Team', to: '/team' },
    { label: 'Jobs Portal', to: '/manage-jobs' },
    { label: 'Interviews Master', to: '/manage-interviews' }
  ],
  global_admin: [
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'Companies', to: '/companies' }
  ]
};

export default function Sidebar() {
  const { user, role, logout } = useAuth();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const menuItems = NAV_MENU[role] || [];

  return (
    <aside className="sidebar-container">
      <div className="sidebar-header">
        <div className="sidebar-brand">InterviewManager</div>
        <div className="sidebar-user-name">{user?.name}</div>
        <div className="sidebar-user-email">{user?.email}</div>
        <div className="sidebar-role-badge">{role?.replace('_', ' ')}</div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map(item => {
          const isActive = pathname === item.to;
          return (
            <button
              key={item.to}
              onClick={() => navigate(item.to)}
              className="sidebar-link"
              style={{
                backgroundColor: isActive ? 'rgba(59, 130, 246, 0.12)' : 'transparent',
                color: isActive ? 'var(--accent)' : 'var(--text-muted)'
              }}
            >
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <button onClick={logout} className="btn btn-ghost" style={{ width: '100%' }}>
          Sign out
        </button>
      </div>
    </aside>
  );
}