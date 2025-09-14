import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

// Upload PDF
export const uploadFile = async (file) => {
  const form = new FormData();
  form.append("file", file);

  try {
    const res = await axios.post(`${API_BASE}/docs/upload`, form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res;
  } catch (err) {
    console.error("Upload failed:", err);
    throw err;
  }
};

// Query API
export const queryAPI = async (query, use_kb = true) => {
  try {
    const res = await axios.post(`${API_BASE}/api/query`, { query, use_kb });
    return res;
  } catch (err) {
    console.error("Query failed:", err);
    throw err;
  }
};
