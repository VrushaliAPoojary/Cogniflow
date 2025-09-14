import React from "react";

export default function ComponentPanel() {
  // static list for now; later add drag-and-drop
  const components = [
    { id: "user", title: "User Query", descr: "Input node for user queries" },
    { id: "kb", title: "KnowledgeBase", descr: "Search docs & embeddings" },
    { id: "llm", title: "LLM Engine", descr: "Call LLM to generate answers" },
    { id: "out", title: "Output", descr: "Display result" },
  ];

  return (
    <div className="space-y-3">
      {components.map((c) => (
        <div
          key={c.id}
          className="p-3 rounded-lg border hover:shadow-md cursor-pointer transition
                     bg-gradient-to-br from-white to-gray-50"
          title={`Drag ${c.title} to the canvas (drag not implemented)`}
        >
          <div className="font-semibold text-gray-800">{c.title}</div>
          <div className="text-sm text-gray-500">{c.descr}</div>
        </div>
      ))}
      <div className="mt-4 text-sm text-gray-500">
        Tip: click nodes in the canvas to edit settings in the right panel.
      </div>
    </div>
  );
}
