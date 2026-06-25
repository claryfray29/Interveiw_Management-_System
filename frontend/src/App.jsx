import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext.jsx';
import Sidebar from './components/Sidebar.jsx';

import Login               from './pages/Login.jsx';
import Dashboard           from './pages/Dashboard.jsx';
import Profile             from './pages/Profile.jsx';
import Jobs                from './pages/Jobs.jsx';
import MyApplications      from './pages/MyApplications.jsx';
import Interviews          from './pages/Interviews.jsx';
import CompanyApplications from './pages/CompanyApplications.jsx';
import CompanyJobs         from './pages/CompanyJobs.jsx';
import Team                from './pages/Team.jsx';
import Schedule            from './pages/Schedule.jsx';
import Companies           from './pages/Companies.jsx';

function Layout() {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard"            element={<Dashboard />} />
          <Route path="profile"              element={<Profile />} />
          <Route path="jobs"                 element={<Jobs />} />
          <Route path="my-applications"      element={<MyApplications />} />
          <Route path="interviews"           element={<Interviews />} />
          <Route path="company/applications" element={<CompanyApplications />} />
          <Route path="company/jobs"         element={<CompanyJobs />} />
          <Route path="company/team"         element={<Team />} />
          <Route path="company/schedule"     element={<Schedule />} />
          <Route path="companies"            element={<Companies />} />
        </Routes>
      </div>
    </div>
  );
}

export default function App() {
  const { token } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={token ? <Navigate to="/dashboard" replace /> : <Login />} />
      <Route path="/*"     element={token ? <Layout /> : <Navigate to="/login" replace />} />
    </Routes>
  );
}