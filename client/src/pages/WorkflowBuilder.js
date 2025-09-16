// client/src/pages/WorkflowBuilder.js
import React, { useState } from "react";
import WorkflowCanvas from "../components/WorkflowCanvas";
import ComponentPanel from "../components/ComponentPanel";
import ConfigPanel from "../components/ConfigPanel";
import { saveWorkflow } from "../api";

export default function WorkflowBuilder() {
  const [workflow, setWorkflow] = useState({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState(null);

  const handleSave = async () => {
    try {
      const res = await saveWorkflow(workflow);
      alert("Workflow saved: " + res.data.id);
    } catch (err) {
      console.error(err);
      alert("Failed to save");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">⚙️ Workflow Builder</h1>
        <div>
          <button onClick={handleSave} className="bg-green-500 text-white px-4 py-2 rounded mr-2">Save</button>
        </div>
      </header>

      <div className="flex flex-1 gap-4 p-6">
        <aside className="w-64 bg-white p-4 rounded shadow">
          <h2 className="font-semibold mb-3">Components</h2>
          <ComponentPanel />
        </aside>

        <main className="flex-1">
          <WorkflowCanvas
            workflow={workflow}
            setWorkflow={setWorkflow}
            setSelectedNode={setSelectedNode}
          />
        </main>

        <aside className="w-80 bg-white p-4 rounded shadow">
          <h2 className="font-semibold mb-3">Configuration</h2>
          <ConfigPanel workflow={workflow} node={selectedNode} />
        </aside>
      </div>
    </div>
  );
}
