// client/src/pages/ChatPage.js
import React, { useState } from "react";
import { queryAPI, uploadFile, runWorkflow } from "../api";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeWorkflow, setActiveWorkflow] = useState(null); // user can set workflow JSON or keep null

  const send = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "you", text: input };
    setMessages(m => [...m, userMessage]);
    setInput("");
    setLoading(true);

    try {
      let res;
      if (activeWorkflow) {
        res = await runWorkflow(activeWorkflow, input);
      } else {
        res = await queryAPI(input, null);
      }
      const answer = res.data?.outputs?.[0]?.text || (res.data && res.data.answer) || JSON.stringify(res.data);
      setMessages(m => [...m, { sender: "bot", text: answer }]);
    } catch (err) {
      console.error(err);
      setMessages(m => [...m, { sender: "bot", text: "⚠️ Error calling API" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Select a file");
    try {
      const resp = await uploadFile(file);
      alert("Uploaded: " + resp.data.filename);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-blue-50 to-gray-100 flex items-center justify-center">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-2xl flex flex-col h-[80vh]">
        <header className="px-6 py-4 border-b flex justify-between items-center bg-blue-600 text-white rounded-t-2xl">
          <h2 className="text-lg font-bold">GenAI Stack Chat</h2>
        </header>

        <div className="flex-1 p-6 overflow-auto space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.sender === "you" ? "justify-end" : "justify-start"}`}>
              <div className={`p-3 rounded-2xl max-w-[75%] ${m.sender === "you" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"}`}>
                {m.text}
              </div>
            </div>
          ))}
          {loading && <div className="text-sm italic text-gray-500">Thinking...</div>}
        </div>

        <div className="p-4 border-t bg-gray-50 rounded-b-2xl">
          <div className="flex gap-2 mb-2">
            <input value={input} onChange={(e)=>setInput(e.target.value)} placeholder="Ask a question..." className="flex-1 border px-3 py-2 rounded" onKeyDown={(e)=>e.key==="Enter" && send()} />
            <button onClick={send} className="bg-blue-600 text-white px-4 py-2 rounded">Send</button>
          </div>

          <div className="flex gap-2 items-center">
            <input type="file" onChange={(e)=>setFile(e.target.files[0])} />
            <button onClick={handleUpload} className="bg-green-600 text-white px-3 py-2 rounded">Upload PDF</button>

            <div className="ml-auto text-sm text-gray-600">
              Tip: If you created a workflow, paste it into `activeWorkflow` variable (developer mode) to run it.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
