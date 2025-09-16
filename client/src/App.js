// client/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import WorkflowBuilder from "./pages/WorkflowBuilder";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow p-4 flex justify-between">
          <h1 className="text-xl font-bold">Cogniflow</h1>
          <nav className="space-x-4">
            <Link to="/" className="text-blue-600">Chat</Link>
            <Link to="/workflow" className="text-blue-600">Workflow Builder</Link>
          </nav>
        </header>

        <main className="p-6">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/workflow" element={<WorkflowBuilder />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
