import React, { useState, useCallback } from "react";
import WorkflowCanvas from "../components/WorkflowCanvas";
import ComponentPanel from "../components/ComponentPanel";
import ConfigPanel from "../components/ConfigPanel";
import { useNavigate } from "react-router-dom";

export default function WorkflowBuilder() {
  const [workflow, setWorkflow] = useState({ nodes: [], edges: [] });
  const navigate = useNavigate();

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <ComponentPanel />
      <div style={{ flex: 1 }}>
        <WorkflowCanvas workflow={workflow} setWorkflow={setWorkflow} />
      </div>
      <ConfigPanel workflow={workflow} setWorkflow={setWorkflow} />
      <div style={{ position: "absolute", bottom: 20, left: 20 }}>
        <button onClick={() => navigate("/chat")}>Chat with Stack</button>
      </div>
    </div>
  );
}
