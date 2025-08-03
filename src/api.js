
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_SERVER,
});

export const getLoginUrl = () => {
  // This is handled by a direct window redirect in the component, 
  // but we can keep the function here for consistency.
  return apiClient.get('/login');
}

export const exchangeCode = (code) => {
  return apiClient.get(`/exchange?code=${code}`);
};

export const getDashboardData = () => {
  return apiClient.get('/dashboard');
};

export const getInsights = (question) => {
  return apiClient.post('/insights', { question });
};
