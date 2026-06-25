import React from 'react';

export default function Modal({ isOpen, onClose, title, children, footerButtons }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span className="modal-title">{title}</span>
          <button className="modal-close-btn" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          {children}
        </div>

        {footerButtons && (
          <div className="modal-footer">
            {footerButtons}
          </div>
        )}
      </div>
    </div>
  );
}