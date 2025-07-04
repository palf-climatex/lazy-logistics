import React from 'react';

function SupplierCard({ supplier, index }) {
  return (
    <div className="bg-white/60 backdrop-blur-sm border border-gray-200/50 rounded-xl p-6 hover:bg-white/80 hover:shadow-md transition-all duration-200">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-sm">
            {supplier.name ? supplier.name.charAt(0).toUpperCase() : 'S'}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {supplier.name}
            </h3>
            {supplier.confidence && (
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                supplier.confidence >= 0.8 ? 'bg-green-100 text-green-800' :
                supplier.confidence >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {Math.round(supplier.confidence * 100)}% confidence
              </span>
            )}
          </div>
          <div className="space-y-2">
            {supplier.context && (
              <p className="text-gray-700 text-sm leading-relaxed">
                {supplier.context}
              </p>
            )}
            {supplier.source_url && (
              <div className="flex items-center space-x-2 text-gray-600">
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                <a
                  href={supplier.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 underline truncate"
                >
                  View source
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SupplierCard; 