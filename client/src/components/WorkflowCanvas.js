import "reactflow/dist/style.css";

import React, { useEffect, useCallback } from "react";
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";

/**
 * Props:
 *  - workflow: { nodes, edges } (optional)
 *  - setWorkflow: function to set workflow (optional)
 *  - setSelectedNode: function(node) when node clicked (optional)
 */
export default function WorkflowCanvas({
  workflow = { nodes: [], edges: [] },
  setWorkflow = () => {},
  setSelectedNode = () => {},
}) {
  // initial demo nodes/edges if workflow empty
  const initialNodes = workflow.nodes.length
    ? workflow.nodes
    : [
        { id: "1", type: "input", data: { label: "User Query" }, position: { x: 50, y: 50 } },
        { id: "2", data: { label: "KnowledgeBase" }, position: { x: 300, y: 150 } },
        { id: "3", data: { label: "LLM Engine" }, position: { x: 600, y: 250 } },
        { id: "4", type: "output", data: { label: "Output" }, position: { x: 900, y: 350 } },
      ];

  const initialEdges = workflow.edges.length
    ? workflow.edges
    : [
        { id: "e1-2", source: "1", target: "2" },
        { id: "e2-3", source: "2", target: "3" },
        { id: "e3-4", source: "3", target: "4" },
      ];

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  // Keep parent workflow in sync, safe-check setWorkflow
  useEffect(() => {
    try {
      if (typeof setWorkflow === "function") setWorkflow({ nodes, edges });
    } catch (e) {
      // defensive: don't crash UI
      console.warn("setWorkflow failed:", e);
    }
  }, [nodes, edges, setWorkflow]);

  // expose node click selection
  const onNodeClick = useCallback((event, node) => {
    try {
      if (typeof setSelectedNode === "function") setSelectedNode(node);
    } catch (e) {
      console.warn("setSelectedNode error:", e);
    }
  }, [setSelectedNode]);

  return (
    <div style={{ height: 600 }} className="w-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        fitView
      >
        <Background color="#e6edf3" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
