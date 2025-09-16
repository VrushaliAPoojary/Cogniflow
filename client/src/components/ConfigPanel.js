// client/src/components/ConfigPanel.js
import React, { useState, useEffect } from "react";

export default function ConfigPanel({ workflow = { nodes: [], edges: [] }, node = null }) {
  const [localData, setLocalData] = useState(node ? node.data : null);

  useEffect(() => {
    setLocalData(node ? node.data : null);
  }, [node]);

  const handleSave = () => {
    if (!node) return;
    // find node in workflow and update its data
    const nidx = workflow.nodes.findIndex(n => n.id === node.id);
    if (nidx === -1) {
      alert("Node not found in workflow");
      return;
    }
    workflow.nodes[nidx].data = localData;
    // This function mutates parent workflow; parent should be aware of update via ReactFlow
    alert("Configuration saved (in memory). Click Save workflow to persist.");
  };

  if (!node) {
    return (
      <div>
        <div className="text-sm">Select a node to edit its settings. Current workflow has <b>{workflow.nodes.length}</b> nodes.</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-2"><strong>Node ID:</strong> {node.id}</div>
      <div className="mb-2"><strong>Type:</strong> {localData?.type || node.type}</div>

      <div className="mb-3">
        <label className="block text-sm font-medium">Prompt</label>
        <textarea rows={6} className="w-full border p-2 rounded" value={localData?.prompt || ""} onChange={(e)=>setLocalData({...localData, prompt:e.target.value})}></textarea>
      </div>

      <div className="flex gap-2">
        <button onClick={handleSave} className="bg-blue-600 text-white px-3 py-2 rounded">Save Config</button>
      </div>
    </div>
  );
}
