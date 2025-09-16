// client/src/components/WorkflowCanvas.js
import React, { useCallback, useRef, useEffect } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";

const nodeTypes = {}; // default nodes - keep basic

export default function WorkflowCanvas({ workflow, setWorkflow, setSelectedNode }) {
  // initialize nodes/edges from workflow prop
  const [nodes, setNodes, onNodesChange] = useNodesState(workflow.nodes || []);
  const [edges, setEdges, onEdgesChange] = useEdgesState(workflow.edges || []);
  const ref = useRef(null);

  useEffect(() => {
    // sync to parent whenever nodes/edges change
    setWorkflow({ nodes, edges });
  }, [nodes, edges, setWorkflow]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const onElementsRemove = (elements) => {
    // remove nodes/edges
    // ReactFlow removeElements changed API — we'll use helper
    // Not using removeElements import to avoid version mismatch; do it manually:
    const ids = new Set(elements.map(e => e.id));
    setNodes((nds) => nds.filter(n => !ids.has(n.id)));
    setEdges((eds) => eds.filter(e => !ids.has(e.id)));
  };

  const onNodeClick = useCallback((evt, node) => {
    setSelectedNode(node);
  }, [setSelectedNode]);

  // Add node programmatically (called by drag-n-drop, or other)
  const addNode = (typeKey) => {
    const id = `${typeKey}_${+new Date()}`;
    const newNode = {
      id,
      type: "default",
      position: { x: 200 + Math.random() * 200, y: 150 + Math.random() * 200 },
      data: { label: typeKey, type: typeKey, prompt: "" },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  // expose addNode via window to be called from ComponentPanel (simple approach)
  useEffect(() => {
    window.__addNode = addNode;
    return () => { window.__addNode = null; };
  }, []);

  return (
    <div className="w-full h-[600px] bg-white rounded shadow p-3">
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          fitView
        >
          <Background gap={20} color="#e6edf3" />
          <Controls />
        </ReactFlow>
      </ReactFlowProvider>
    </div>
  );
}
