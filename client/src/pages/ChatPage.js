import React, { useState } from "react";
import { queryAPI, uploadFile } from "../api";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "you", text: input };
    setMessages((m) => [...m, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await queryAPI(input, true);
      const botMessage = { sender: "bot", text: res.data.answer };
      setMessages((m) => [...m, botMessage]); // ✅ prevent duplicate user message
    } catch (err) {
      console.error(err);
      setMessages((m) => [...m, { sender: "bot", text: "⚠️ Error calling API" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      const resp = await uploadFile(file);
      alert("Uploaded: " + resp.data.filename);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">💬 Chat</h2>

        {/* Chat messages */}
        <div className="space-y-3 mb-4">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`p-3 rounded-lg max-w-[80%] ${
                m.sender === "you"
                  ? "ml-auto bg-blue-500 text-white"
                  : "mr-auto bg-gray-200 text-gray-800"
              }`}
            >
              <b>{m.sender === "you" ? "You" : "Bot"}:</b> {m.text}
            </div>
          ))}
          {loading && (
            <div className="italic text-gray-500">Bot is typing...</div>
          )}
        </div>

        {/* Input box */}
        <div className="flex gap-2 mb-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring focus:ring-blue-400 outline-none"
            onKeyDown={(e) => e.key === "Enter" && send()}
          />
          <button
            onClick={send}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            Send
          </button>
        </div>

        {/* Upload PDF */}
        <div className="flex items-center gap-2">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="flex-1 text-sm"
          />
          <button
            onClick={handleUpload}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
          >
            Upload PDF
          </button>
        </div>
      </div>
    </div>
  );
}
