import React from 'react';

export default function Spinner({ message = 'Loading...' }) {
  return (
    <div className="spinner-container">
      <div className="spinner-element"></div>
      {message && <span className="spinner-message">{message}</span>}
    </div>
  );
}