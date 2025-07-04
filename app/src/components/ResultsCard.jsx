import React from 'react';
import SupplierCard from './SupplierCard';

function ResultsCard({ data }) {
  if (!data) return null;

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Extracted Suppliers</h2>
          {data.total_suppliers && (
            <p className="text-gray-600 text-sm mt-1">
              Found {data.total_suppliers} suppliers in {data.processing_time?.toFixed(2)}s
            </p>
          )}
        </div>
      </div>

      {data.suppliers && Array.isArray(data.suppliers) && data.suppliers.length > 0 ? (
        <div className="grid gap-4">
          {data.suppliers.map((supplier, index) => (
            <SupplierCard key={index} supplier={supplier} index={index} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33" />
            </svg>
          </div>
          <p className="text-gray-500 text-lg">No suppliers found</p>
          <p className="text-gray-400 text-sm mt-1">Try a different company name</p>
        </div>
      )}
    </div>
  );
}

export default ResultsCard; 