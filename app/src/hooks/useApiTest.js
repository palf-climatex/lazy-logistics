import { useState } from 'react';
import { supplierApi } from '../api';

export const useApiTest = () => {
  const [apiTestSuccess, setApiTestSuccess] = useState(false);

  const testDirectAPI = async () => {
    try {
      console.log('Testing direct API call with "tesco"');
      const data = await supplierApi.testConnection();
      console.log('Direct API response:', data);
      setApiTestSuccess(true);
    } catch (error) {
      console.error('Direct API test failed:', error);
      setApiTestSuccess(false);
    }
  };

  const resetApiTest = () => {
    setApiTestSuccess(false);
  };

  return {
    apiTestSuccess,
    testDirectAPI,
    resetApiTest
  };
}; 