// client/src/components/ComponentPanel.js
import React from "react";

export default function ComponentPanel() {
  const components = [
    { id: "user", title: "User Query", descr: "Input node for user queries" },
    { id: "kb", title: "KnowledgeBase", descr: "Search docs & embeddings" },
    { id: "llm", title: "LLM Engine", descr: "Use local LLM" },
    { id: "websearch", title: "Web Search", descr: "Optional web search node" },
    { id: "output", title: "Output", descr: "Display final result" },
  ];

  const handleAdd = (id) => {
    // call the global addNode from WorkflowCanvas
    if (window.__addNode) window.__addNode(id);
  };

  return (
    <div className="space-y-3">
      {components.map(c => (
        <div key={c.id} className="p-3 rounded border hover:shadow cursor-pointer" onClick={() => handleAdd(c.id)}>
          <div className="font-semibold">{c.title}</div>
          <div className="text-sm text-gray-600">{c.descr}</div>
        </div>
      ))}
      <div className="mt-4 text-xs text-gray-500">Click to add to canvas. Connect nodes by dragging from node handles.</div>
    </div>
  );
}
