import React from 'react';

function ErrorCard({ error }) {
  if (!error) return null;

  return (
    <div className="bg-red-50/80 backdrop-blur-sm border border-red-200 rounded-2xl p-6 mb-8">
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-red-800">Error</h3>
          <p className="text-red-700 mt-1">{error.message}</p>
        </div>
      </div>
    </div>
  );
}

export default ErrorCard; 