import React from "react";

export default function ConfigPanel({ workflow = { nodes: [], edges: [] }, node = null }) {
  return (
    <div>
      {node ? (
        <div>
          <h3 className="text-md font-semibold mb-2">Selected Node</h3>
          <div className="p-3 border rounded bg-gray-50">
            <div><strong>ID:</strong> {node.id}</div>
            <div><strong>Type:</strong> {node.type || "default"}</div>
            <div className="mt-2 text-sm text-gray-700">
              <strong>Data:</strong>
              <pre className="text-xs mt-1 overflow-auto max-h-40 bg-white p-2 rounded">{JSON.stringify(node.data, null, 2)}</pre>
            </div>
          </div>
        </div>
      ) : (
        <div>
          <h3 className="text-md font-semibold mb-2">Workflow</h3>
          <div className="p-3 border rounded bg-gray-50 text-sm">
            <div><strong>Nodes:</strong> {workflow.nodes?.length || 0}</div>
            <div><strong>Edges:</strong> {workflow.edges?.length || 0}</div>
            <div className="mt-3">
              <strong>Full data:</strong>
              <pre className="text-xs mt-1 overflow-auto max-h-56 bg-white p-2 rounded">{JSON.stringify(workflow, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
