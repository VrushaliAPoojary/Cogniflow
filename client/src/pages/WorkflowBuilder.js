import React, { useState } from "react";
import WorkflowCanvas from "../components/WorkflowCanvas";
import ComponentPanel from "../components/ComponentPanel";
import ConfigPanel from "../components/ConfigPanel";

export default function WorkflowBuilder() {
  // central workflow state (nodes + edges)
  const [workflow, setWorkflow] = useState({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState(null);

  const handleSave = () => {
    // TODO: persist to server (POST /workflows/save)
    console.log("Saving workflow:", workflow);
    alert("Workflow saved (console logged).");
  };

  const handleRun = () => {
    // TODO: call run endpoint or execute locally
    console.log("Running workflow:", workflow);
    alert("Workflow run started (console logged).");
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">⚙️ Workflow Builder</h1>
        <div className="space-x-3">
          <button
            onClick={handleSave}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg shadow"
          >
            Save
          </button>
          <button
            onClick={handleRun}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow"
          >
            Run
          </button>
        </div>
      </header>

      {/* Main layout */}
      <div className="flex flex-1">
        {/* Left Sidebar */}
        <aside className="w-64 bg-white border-r shadow-lg p-4">
          <h2 className="text-lg font-semibold mb-3">🧩 Components</h2>
          <ComponentPanel />
        </aside>

        {/* Canvas */}
        <main className="flex-1 relative p-6">
          <div className="h-full rounded-lg overflow-hidden bg-white shadow">
            {/* grid background wrapper */}
            <div className="h-full bg-grid">
              <WorkflowCanvas
                workflow={workflow}
                setWorkflow={setWorkflow}
                setSelectedNode={setSelectedNode}
              />
            </div>
          </div>
        </main>

        {/* Config Panel */}
        <aside className="w-72 bg-white border-l shadow-lg p-4">
          <h2 className="text-lg font-semibold mb-3">⚙️ Configuration</h2>
          <ConfigPanel workflow={workflow} node={selectedNode} />
        </aside>
      </div>
    </div>
  );
}
