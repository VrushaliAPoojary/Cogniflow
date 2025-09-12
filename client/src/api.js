import axios from "axios";
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export const uploadFile = (file) => {
  const form = new FormData();
  form.append("file", file);
  return axios.post(`${API_BASE}/docs/upload`, form, { headers: { "Content-Type": "multipart/form-data" } });
};

export const queryAPI = (query, use_kb = true) => {
  return axios.post(`${API_BASE}/api/query`, { query, use_kb });
};
