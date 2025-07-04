import { useState } from 'react';
import useSWR from 'swr';
import { supplierApi } from '../api';

export const useSupplierExtraction = () => {
  const [companyName, setCompanyName] = useState('');
  const [shouldFetch, setShouldFetch] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const { data, error, isLoading } = useSWR(
    shouldFetch ? `extract-suppliers-${searchTerm}` : null,
    () => supplierApi.extractSuppliers(searchTerm),
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      shouldRetryOnError: false
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (companyName.trim()) {
      console.log('Submitting company name:', companyName);
      setSearchTerm(companyName.trim());
      setShouldFetch(true);
    }
  };

  const handleReset = () => {
    setCompanyName('');
    setSearchTerm('');
    setShouldFetch(false);
  };

  return {
    companyName,
    setCompanyName,
    data,
    error,
    isLoading,
    handleSubmit,
    handleReset
  };
}; 