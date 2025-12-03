// src/services/api.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
});

// Attach token to outgoing requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
}, (err) => Promise.reject(err));

// Central response error handling (can be extended)
api.interceptors.response.use(res => res, (error) => {
  if (!error.response) return Promise.reject(error);
  // Example: handle 401 globally
  if (error.response.status === 401) {
    // optional: auto sign out
    localStorage.removeItem("token");
    // window.location = "/login";
  }
  return Promise.reject(error);
});

export default api;
