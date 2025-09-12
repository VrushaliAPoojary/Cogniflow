import React from "react";

export default function ConfigPanel({ workflow }) {
  return (
    <div style={{ width: 300, borderLeft: "1px solid #ddd", padding: 16 }}>
      <h3>Config</h3>
      <pre style={{ fontSize: 12, maxHeight: "80vh", overflow: "auto" }}>{JSON.stringify(workflow, null, 2)}</pre>
    </div>
  );
}
