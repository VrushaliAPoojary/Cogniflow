import React, { useState } from "react";
import ReactFlow, { Background, Controls, addEdge } from "reactflow";
import "reactflow/dist/style.css";

const initialNodes = [
  { id: "1", type: "input", data: { label: "User Query" }, position: { x: 50, y: 50 } },
  { id: "2", data: { label: "KnowledgeBase" }, position: { x: 300, y: 150 } },
  { id: "3", data: { label: "LLM Engine" }, position: { x: 600, y: 250 } },
  { id: "4", type: "output", data: { label: "Output" }, position: { x: 900, y: 350 } },
];

export default function WorkflowCanvas({ workflow, setWorkflow }) {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState([
    { id: "e1-2", source: "1", target: "2" },
    { id: "e2-3", source: "2", target: "3" },
    { id: "e3-4", source: "3", target: "4" },
  ]);

  const onConnect = (params) => {
    setEdges((eds) => addEdge(params, eds));
  };

  const onNodesChange = (changes) => {};
  const onEdgesChange = (changes) => {};

  React.useEffect(() => {
    setWorkflow({ nodes, edges });
  }, [nodes, edges]);

  return (
    <div style={{ height: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
