import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WorkflowBuilder from "./pages/WorkflowBuilder";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <Router>
      {/* Simple Navbar */}
      <header style={{ padding: "12px", background: "#2d3436", color: "white" }}>
        <nav style={{ display: "flex", gap: "20px" }}>
          <Link to="/" style={{ color: "white", textDecoration: "none" }}>
            ⚙️ Workflow Builder
          </Link>
          <Link to="/chat" style={{ color: "white", textDecoration: "none" }}>
            💬 Chat
          </Link>
        </nav>
      </header>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<WorkflowBuilder />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="*" element={<h2 style={{ textAlign: "center", marginTop: "20px" }}>404 - Page Not Found</h2>} />
      </Routes>
    </Router>
  );
}

export default App;
