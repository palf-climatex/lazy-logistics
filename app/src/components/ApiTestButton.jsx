import React from 'react';

function ApiTestButton({ onTest, apiTestSuccess }) {
  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 backdrop-blur-sm rounded-2xl shadow-xl border border-blue-200/30 p-6 mb-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800">API Connection</h3>
            <p className="text-sm text-gray-600">Test the backend API connection</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button
            type="button"
            onClick={onTest}
            className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-4 focus:ring-gray-500/20 transition-all duration-200 font-semibold"
          >
            🧪 Test Connection
          </button>
          {apiTestSuccess && (
            <div className="flex items-center space-x-2 bg-green-100 text-green-700 px-4 py-2 rounded-full">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-sm font-medium">Connected</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ApiTestButton; 