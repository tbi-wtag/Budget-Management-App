import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export const getCategories = () => API.get('/categories/');
export const createCategory = (data) => API.post('/categories/', data);
export const deleteCategory = (id) => API.delete(`/categories/${id}`);

export const getTransactions = () => API.get('/transactions/');
export const createTransaction = (data) => API.post('/transactions/', data);
export const deleteTransaction = (id) => API.delete(`/transactions/${id}`);

export const getSummary = (month) => API.get(`/summary?month=${month}`);