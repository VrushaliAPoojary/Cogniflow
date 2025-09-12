import React from "react";

export default function ComponentPanel() {
  return (
    <div style={{ width: 200, borderRight: "1px solid #ddd", padding: 16 }}>
      <h3>Components</h3>
      <ul>
        <li>User Query</li>
        <li>KnowledgeBase</li>
        <li>LLM Engine</li>
        <li>Output</li>
      </ul>
      <p>Drag items to canvas (drag support can be expanded later).</p>
    </div>
  );
}
