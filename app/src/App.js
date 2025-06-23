import React, { useState } from 'react';
import useSWR from 'swr';

const fetcher = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data); // Debug log
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

function App() {
  const [companyName, setCompanyName] = useState('');
  const [shouldFetch, setShouldFetch] = useState(false);

  const { data, error, isLoading } = useSWR(
    shouldFetch ? ['http://localhost:8000/extract-suppliers', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ company_name: companyName })
    }] : null,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      shouldRetryOnError: false
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (companyName.trim()) {
      console.log('Submitting company name:', companyName); // Debug log
      setShouldFetch(true);
    }
  };

  const handleReset = () => {
    setCompanyName('');
    setShouldFetch(false);
  };

  const testDirectAPI = async () => {
    try {
      console.log('Testing direct API call with "tesco"');
      const response = await fetch('http://localhost:8000/extract-suppliers', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ company_name: 'tesco' })
      });
      const data = await response.json();
      console.log('Direct API response:', data);
      alert(`Direct API test successful! Found ${data.total_suppliers} suppliers.`);
    } catch (error) {
      console.error('Direct API test failed:', error);
      alert(`Direct API test failed: ${error.message}`);
    }
  };

  console.log('Current state:', { companyName, shouldFetch, data, error, isLoading }); // Debug log

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
            Lazy Logistics UI
          </h1>
          <p className="text-gray-600 text-lg">Extract supplier information with ease</p>
        </div>
        
        {/* Form Card */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="companyName" className="block text-sm font-semibold text-gray-700 mb-3">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                  <span>Company Name</span>
                </div>
              </label>
              <input
                type="text"
                id="companyName"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-200 text-gray-700 placeholder-gray-400"
                placeholder="Enter company name to extract suppliers..."
                required
              />
            </div>
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Extracting...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <span>Extract Suppliers</span>
                  </div>
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-4 focus:ring-gray-500/20 transition-all duration-200 font-semibold"
              >
                Reset
              </button>
            </div>
            <div className="pt-4 border-t border-gray-200">
              <button
                type="button"
                onClick={testDirectAPI}
                className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500/20 transition-all duration-200 text-sm"
              >
                🧪 Test API Connection (Tesco)
              </button>
            </div>
          </form>
        </div>

        {/* Error Card */}
        {error && (
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
        )}

        {/* Results Card */}
        {data && (
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
                  <div key={index} className="bg-white/60 backdrop-blur-sm border border-gray-200/50 rounded-xl p-6 hover:bg-white/80 hover:shadow-md transition-all duration-200">
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
        )}
      </div>
    </div>
  );
}

export default App; 