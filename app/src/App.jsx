import React from 'react';
import { useSupplierExtraction, useApiTest } from './hooks';
import Header from './components/Header';
import ApiTestButton from './components/ApiTestButton';
import SupplierForm from './components/SupplierForm';
import ErrorCard from './components/ErrorCard';
import ResultsCard from './components/ResultsCard';

function App() {
  const {
    companyName,
    setCompanyName,
    data,
    error,
    isLoading,
    handleSubmit,
    handleReset
  } = useSupplierExtraction();

  const {
    apiTestSuccess,
    testDirectAPI,
    resetApiTest
  } = useApiTest();

  const handleFormReset = () => {
    handleReset();
    resetApiTest();
  };

  console.log('Current state:', { companyName, data, error, isLoading }); // Debug log

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <Header />
        <ApiTestButton onTest={testDirectAPI} apiTestSuccess={apiTestSuccess} />
        <SupplierForm
          companyName={companyName}
          setCompanyName={setCompanyName}
          onSubmit={handleSubmit}
          onReset={handleFormReset}
          isLoading={isLoading}
        />
        <ErrorCard error={error} />
        <ResultsCard data={data} />
      </div>
    </div>
  );
}

export default App;
