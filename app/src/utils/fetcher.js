export const fetcher = async (url, options) => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data); // Debug log
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out after 30 seconds');
    }
    throw error;
  }
}; 