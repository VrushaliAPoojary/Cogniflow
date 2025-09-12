import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WorkflowBuilder from "./pages/WorkflowBuilder";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WorkflowBuilder />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
}

export default App;
