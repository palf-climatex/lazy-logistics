import { fetcher } from '../utils/fetcher';

const API_BASE_URL = 'http://localhost:8000';

export const supplierApi = {
  /**
   * Extract suppliers for a given company
   * @param {string} companyName - The name of the company to extract suppliers for
   * @returns {Promise<Object>} - The API response with supplier data
   */
  extractSuppliers: async (companyName) => {
    return fetcher(`${API_BASE_URL}/extract-suppliers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ company_name: companyName })
    });
  },

  /**
   * Test API connection with a sample company (tesco)
   * @returns {Promise<Object>} - The API response
   */
  testConnection: async () => {
    return fetcher(`${API_BASE_URL}/extract-suppliers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ company_name: 'tesco' })
    });
  }
}; 