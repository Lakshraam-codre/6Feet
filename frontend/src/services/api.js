import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat endpoints
export const sendChatMessage = (farmerId, message, channel = 'web', language = 'english') => {
  return apiClient.post('/channels/web/chat', {
    farmer_id: farmerId,
    message,
    channel,
    language,
  });
};

// Weather endpoints
export const getWeather = (location) => {
  return apiClient.get(`/channels/web/weather/${location}`);
};

// Market endpoints
export const getMarketPrice = (cropName, location = null) => {
  return apiClient.get(`/channels/web/market/${cropName}`, {
    params: { location },
  });
};

// Admin endpoints
export const getFarmers = (skip = 0, limit = 100) => {
  return apiClient.get('/admin/farmers', {
    params: { skip, limit },
  });
};

export const getFarmer = (farmerId) => {
  return apiClient.get(`/admin/farmers/${farmerId}`);
};

export const createFarmer = (farmerData) => {
  return apiClient.post('/admin/farmers', farmerData);
};

export const updateFarmer = (farmerId, farmerData) => {
  return apiClient.put(`/admin/farmers/${farmerId}`, farmerData);
};

export const getMarketPrices = (crop = null, location = null) => {
  return apiClient.get('/admin/market-prices', {
    params: { crop, location },
  });
};

export const createMarketPrice = (priceData) => {
  return apiClient.post('/admin/market-prices', priceData);
};

export const deleteMarketPrice = (priceId) => {
  return apiClient.delete(`/admin/market-prices/${priceId}`);
};

export const createAlert = (alertData) => {
  return apiClient.post('/admin/alerts', alertData);
};

export const sendBulkAlerts = (alertData, locationFilter = null) => {
  return apiClient.post('/admin/alerts/send-bulk', alertData, {
    params: { location_filter: locationFilter },
  });
};

export const getStatistics = () => {
  return apiClient.get('/admin/stats');
};

export default apiClient;
