// client/src/api.js
import axios from "axios";
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export const uploadFile = async (file) => {
  const form = new FormData();
  form.append("file", file);
  return await axios.post(`${API_BASE}/docs/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const queryAPI = async (query, workflow = null) => {
  const body = { query, workflow };
  return await axios.post(`${API_BASE}/api/query`, body);
};

export const saveWorkflow = async (wf) => {
  return await axios.post(`${API_BASE}/workflows/save`, wf);
};

export const runWorkflow = async (workflow, query) => {
  return await axios.post(`${API_BASE}/workflows/run`, { workflow, query });
};

export { API_BASE };
